#!/usr/bin/env node
/**
 * Fetch open BasedAgents tasks and write BOARD_SNAPSHOT.md.
 *
 * A commit happens only when the open-task set changes (task id, title,
 * category, created_at, bounty). A second run against the same board leaves
 * the file untouched, so git commits nothing.
 */

import { createHash } from 'node:crypto';
import { execFileSync } from 'node:child_process';
import { existsSync, readFileSync, writeFileSync } from 'node:fs';

const API = (process.env.BASEDAGENTS_API_URL || 'https://api.basedagents.ai').replace(/\/$/, '');
const OUT = process.env.SNAPSHOT_OUT || 'BOARD_SNAPSHOT.md';
const PAGE = 100;
const MAX_PAGES = 50;
const FINGERPRINT_RE = /<!-- board-fingerprint: ([a-f0-9]{64}) -->/;

function log(line) {
  console.log(line);
}

async function fetchOpenTasks() {
  const tasks = [];
  for (let page = 0; page < MAX_PAGES; page++) {
    const offset = page * PAGE;
    const url = `${API}/v1/tasks?status=open&limit=${PAGE}&offset=${offset}`;
    const res = await fetch(url, {
      headers: {
        Accept: 'application/json',
        'User-Agent': 'ba-board-snapshot/1.0',
      },
    });
    if (!res.ok) {
      const body = await res.text();
      throw new Error(`GET ${url} failed: ${res.status} ${body.slice(0, 300)}`);
    }
    const data = await res.json();
    const batch = Array.isArray(data.tasks) ? data.tasks : null;
    if (!batch) throw new Error(`GET ${url} returned no tasks array`);
    tasks.push(...batch);
    log(`Fetched ${batch.length} tasks (offset ${offset})`);
    if (batch.length < PAGE) return tasks;
  }
  throw new Error(`Stopped after ${MAX_PAGES} pages (${tasks.length} tasks)`);
}

function formatBounty(task) {
  const bounty = task.bounty;
  if (bounty && bounty.amount_display) {
    const token = bounty.token || 'USDC';
    return `${bounty.amount_display} ${token}`;
  }
  return 'free';
}

function formatAge(createdAt, nowMs) {
  const created = Date.parse(createdAt);
  if (!Number.isFinite(created)) return 'unknown';
  const ms = Math.max(0, nowMs - created);
  const minutes = Math.floor(ms / 60_000);
  if (minutes < 1) return '<1m';
  if (minutes < 60) return `${minutes}m`;
  const hours = Math.floor(minutes / 60);
  if (hours < 48) return `${hours}h`;
  return `${Math.floor(hours / 24)}d`;
}

function escapeCell(value) {
  return String(value ?? '')
    .replace(/\r?\n/g, ' ')
    .replace(/\|/g, '\\|')
    .trim();
}

function fingerprintOf(tasks) {
  const rows = tasks
    .map((task) => ({
      task_id: String(task.task_id ?? ''),
      title: String(task.title ?? ''),
      category: String(task.category ?? ''),
      created_at: String(task.created_at ?? ''),
      bounty: formatBounty(task),
    }))
    .sort((a, b) => (a.task_id < b.task_id ? -1 : a.task_id > b.task_id ? 1 : 0));
  return createHash('sha256').update(JSON.stringify(rows)).digest('hex');
}

function render(tasks, nowMs) {
  const fingerprint = fingerprintOf(tasks);
  const generated = new Date(nowMs).toISOString().replace(/\.\d{3}Z$/, 'Z');
  const date = generated.slice(0, 10);
  const counts = new Map();
  for (const task of tasks) {
    const category = task.category || 'uncategorized';
    counts.set(category, (counts.get(category) || 0) + 1);
  }
  const countRows = [...counts.entries()]
    .sort((a, b) => (a[0] < b[0] ? -1 : a[0] > b[0] ? 1 : 0))
    .map(([category, count]) => `| ${escapeCell(category)} | ${count} |`);

  const tableRows = [...tasks]
    .sort((a, b) => {
      const byCreated = String(b.created_at ?? '').localeCompare(String(a.created_at ?? ''));
      if (byCreated !== 0) return byCreated;
      return String(a.task_id ?? '').localeCompare(String(b.task_id ?? ''));
    })
    .map((task) => {
      const title = escapeCell(task.title || '(untitled)');
      const category = escapeCell(task.category || 'uncategorized');
      const age = formatAge(task.created_at, nowMs);
      const bounty = escapeCell(formatBounty(task));
      return `| ${title} | ${category} | ${age} | ${bounty} |`;
    });

  const lines = [
    '# BasedAgents board snapshot',
    '',
    `- Date: ${date}`,
    `- Generated: ${generated}`,
    `- Open tasks: ${tasks.length}`,
    '',
    '## Count by category',
    '',
    '| Category | Open |',
    '| --- | ---: |',
    ...(countRows.length ? countRows : ['| (none) | 0 |']),
    '',
    '## Open tasks',
    '',
    '| Title | Category | Age | Bounty |',
    '| --- | --- | --- | --- |',
    ...(tableRows.length ? tableRows : ['| (none) |  |  |  |']),
    '',
    `<!-- board-fingerprint: ${fingerprint} -->`,
    '',
  ];
  return { markdown: lines.join('\n'), fingerprint };
}

function existingFingerprint() {
  if (!existsSync(OUT)) return null;
  const match = FINGERPRINT_RE.exec(readFileSync(OUT, 'utf8'));
  return match ? match[1] : null;
}

function inGitRepo() {
  try {
    execFileSync('git', ['rev-parse', '--is-inside-work-tree'], { stdio: 'ignore' });
    return true;
  } catch {
    return false;
  }
}

function git(args) {
  try {
    return execFileSync('git', args, {
      encoding: 'utf8',
      stdio: ['ignore', 'pipe', 'pipe'],
    }).trim();
  } catch (err) {
    const stderr = err.stderr ? err.stderr.toString().trim() : '';
    throw new Error(`git ${args.join(' ')} failed${stderr ? `: ${stderr}` : ''}`);
  }
}

function cachedDiffExists() {
  try {
    execFileSync('git', ['diff', '--cached', '--quiet', '--', OUT], { stdio: 'ignore' });
    return false;
  } catch {
    return true;
  }
}

function gitAllowFail(args) {
  try {
    return execFileSync('git', args, {
      encoding: 'utf8',
      stdio: ['ignore', 'pipe', 'pipe'],
    }).trim();
  } catch {
    return '';
  }
}

function commitIfChanged() {
  if (!inGitRepo()) {
    log('Not a git repository; file written, commit skipped.');
    return;
  }
  const shouldCommit = process.env.GITHUB_ACTIONS === 'true' || process.env.SNAPSHOT_COMMIT === '1';
  if (!shouldCommit) {
    log('SNAPSHOT_COMMIT is not set; file written, commit left to the caller.');
    return;
  }
  git(['add', '--', OUT]);
  if (!cachedDiffExists()) {
    log('Working tree matches HEAD; commit skipped.');
    return;
  }
  if (!gitAllowFail(['config', '--get', 'user.name'])) {
    execFileSync('git', ['config', 'user.name', 'github-actions[bot]'], { stdio: 'ignore' });
  }
  if (!gitAllowFail(['config', '--get', 'user.email'])) {
    execFileSync('git', ['config', 'user.email', '41898282+github-actions[bot]@users.noreply.github.com'], {
      stdio: 'ignore',
    });
  }
  git(['commit', '-m', 'chore: weekly board snapshot']);
  const sha = git(['rev-parse', '--short', 'HEAD']);
  log(`Committed ${sha}`);
  if (process.env.SNAPSHOT_NO_PUSH === '1') {
    log('SNAPSHOT_NO_PUSH=1; push skipped.');
    return;
  }
  const branch = process.env.GITHUB_REF_NAME || git(['rev-parse', '--abbrev-ref', 'HEAD']);
  git(['push', 'origin', `HEAD:${branch}`]);
  log(`Pushed HEAD to origin/${branch}`);
}

async function main() {
  log(`Snapshot source: ${API}/v1/tasks?status=open`);
  const tasks = await fetchOpenTasks();
  const { markdown, fingerprint } = render(tasks, Date.now());
  log(`Open tasks: ${tasks.length}`);
  log(`Fingerprint: ${fingerprint}`);
  const previous = existingFingerprint();
  if (previous === fingerprint) {
    log('Board unchanged; commit skipped.');
    return;
  }
  writeFileSync(OUT, markdown);
  log(`Wrote ${OUT}`);
  commitIfChanged();
}

main().catch((err) => {
  console.error(err instanceof Error ? err.message : String(err));
  process.exit(1);
});
