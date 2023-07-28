import { setFailed, setOutput } from '@actions/core';
import * as toml from 'toml';
async function run() {
    let { REPOSITORY: repository } = process.env
    if (!repository) throw new Error('REPOSITORY env var is not set')
    if (repository.includes('https://raw.githubusercontent.com/')) {
        try {
            console.log(repository);
            const response = await fetch(new URL(repository.replace(/[<>]/g, '')));
            const data = await response.text();
            const parsed = toml.parse(data);
            const content = {
                "name": parsed.project.name,
                "description": parsed.project.description,
                "version": parsed.project.version,
                "tags": parsed.project.keywords,
                "url": parsed.project.urls.Repository,
                "author": parsed.project.authors[0].name,
                "pip": parsed.project.name,
                "vertified": false,
                "type": "plugin"
            }
            console.log(content);
            setOutput('validation_output',{
                "result": "success",
                "content": content,
                "repository": repository,
            });
        } catch (e) {
            setFailed(e);
            return;
        }
    }else{
        setOutput('validation_output',{
            "result": "failure",
            "content": "Not a valid repository",
            "repository": repository,
        });
    }
    return;
}

await run();

