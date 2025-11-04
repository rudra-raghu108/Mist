#!/usr/bin/env node

import { spawn } from 'child_process';

const processes = [];
let exiting = false;

function startProcess(name, command, args) {
  const child = spawn(command, args, {
    stdio: 'inherit',
    shell: true,
    env: {
      ...process.env,
      FORCE_COLOR: process.env.FORCE_COLOR ?? '1',
    },
  });

  processes.push({ name, child });

  child.on('exit', (code, signal) => {
    if (exiting) {
      return;
    }

    exiting = true;
    if (signal) {
      console.log(`\n${name} exited with signal ${signal}`);
    } else if (code !== 0) {
      console.error(`\n${name} exited with code ${code}`);
    }

    for (const proc of processes) {
      if (proc.child.pid && !proc.child.killed) {
        proc.child.kill('SIGTERM');
      }
    }

    process.exit(code ?? (signal ? 1 : 0));
  });
}

function handleShutdown(signal) {
  if (exiting) return;
  exiting = true;

  console.log(`\nReceived ${signal}. Shutting down...`);
  for (const proc of processes) {
    if (proc.child.pid && !proc.child.killed) {
      proc.child.kill(signal);
    }
  }
}

process.on('SIGINT', () => handleShutdown('SIGINT'));
process.on('SIGTERM', () => handleShutdown('SIGTERM'));

startProcess('backend', 'npm', ['run', 'dev:backend']);
startProcess('frontend', 'npm', ['run', 'dev']);
