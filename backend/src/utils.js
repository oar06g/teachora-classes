import fs from "fs";
import path from "path";

export function readFileSync(path) {
  return fs.readFileSync(path, 'utf8');
}

export function pathFile(dir, filename) {
  return path.join(dir, filename);
}