// Shared loader for the TypeScript reproduction checks.
//
// The checks import the fixture's .ts modules directly. Node 22.6 and later can
// strip TypeScript type annotations at load time; run every check as
//
//   node --experimental-strip-types checks/<id>.mjs REPO
//
// (score.py --verify-fixes does this). The fixture's TypeScript uses only
// erasable syntax (annotations, interfaces, type arguments), which this mode
// supports. Exit status of every check: 0 when correct, 1 when the wrong output
// is reproduced, 2 on a usage or load error.

import path from "node:path";
import { pathToFileURL } from "node:url";

export async function loadModule(relativePath) {
  const repo = process.argv[2];
  if (!repo) {
    console.error("usage: node --experimental-strip-types <check>.mjs REPO");
    process.exit(2);
  }
  try {
    return await import(pathToFileURL(path.resolve(repo, relativePath)).href);
  } catch (error) {
    console.error(`cannot load ${relativePath}: ${error.message}`);
    process.exit(2);
  }
}

export function pass(message) {
  console.log(`PASS: ${message}`);
  process.exit(0);
}

export function fail(message) {
  console.log(`FAIL: ${message}`);
  process.exit(1);
}
