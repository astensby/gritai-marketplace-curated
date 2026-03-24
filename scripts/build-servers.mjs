#!/usr/bin/env node

/**
 * Build script for custom MCP servers.
 *
 * Installs dependencies, then bundles each server's TypeScript source into a
 * single self-contained JS file using esbuild. The output includes all
 * dependencies inlined (no node_modules needed at runtime).
 *
 * Usage:
 *   node scripts/build-servers.mjs              # Build all servers
 *   node scripts/build-servers.mjs nanobanana   # Build specific server
 */

import { build } from "esbuild";
import { existsSync } from "fs";
import { resolve, dirname } from "path";
import { fileURLToPath } from "url";
import { execSync } from "child_process";

const __dirname = dirname(fileURLToPath(import.meta.url));
const ROOT = resolve(__dirname, "..");

const SERVERS = [
  {
    name: "nanobanana",
    plugin: "gritai-image-gen",
    serverDir: "servers/nanobanana",
    entry: "servers/nanobanana/src/index.ts",
    outfile: "servers/nanobanana/dist/index.js",
  },
];

const targetName = process.argv[2];

for (const server of SERVERS) {
  if (targetName && server.name !== targetName) continue;

  const pluginDir = resolve(ROOT, "plugins", server.plugin);
  const serverDir = resolve(pluginDir, server.serverDir);
  const entryPoint = resolve(pluginDir, server.entry);
  const outfile = resolve(pluginDir, server.outfile);

  if (!existsSync(entryPoint)) {
    console.error(`[SKIP] ${server.name}: entry not found at ${entryPoint}`);
    continue;
  }

  // Install dependencies if needed
  if (!existsSync(resolve(serverDir, "node_modules"))) {
    console.log(`[DEPS] ${server.name}: installing dependencies...`);
    execSync("npm install --ignore-scripts", { cwd: serverDir, stdio: "pipe" });
  }

  console.log(`[BUILD] ${server.name} → ${server.outfile}`);

  await build({
    entryPoints: [entryPoint],
    outfile,
    bundle: true,
    platform: "node",
    target: "node18",
    format: "esm",
    sourcemap: false,
    minify: true,
    treeShaking: true,
  });

  console.log(`[DONE] ${server.name}`);
}

console.log("\nAll servers built successfully.");
