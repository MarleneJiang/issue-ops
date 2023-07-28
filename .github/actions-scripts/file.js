import * as core from '@actions/core';
import fs from 'fs';

async function run() {
  try {
    let { FILE: file, VALUES:values } = process.env;
    let data = fs.readFileSync(file, 'utf8');
    let obj = JSON.parse(data);
    obj['data'].push(JSON.parse(values));
    console.log(obj);
    data = JSON.stringify(obj, null, 2);
    fs.writeFileSync(file, data, 'utf8');
  } catch (error) {
    if (error instanceof Error) core.setFailed(error.message);
  }
}

run();