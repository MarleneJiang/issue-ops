import {setFailed, setOutput} from '@actions/core';

function run() {
    let { REPOSITORY: repository } = process.env
    if (!repository) throw new Error('REPOSITORY env var is not set')
    console.log(repository)
    setFailed("test~~~~~")
    if (repository.includes('http')) {
        try {
            // When parsed the url will be like <https://hub.docker.com>
            const url = new URL(repository.replace(/[<>]/g, ''));
        } catch (e) {
            setFailed(e);

            return;
        }
    }


    setOutput('repository', repository);
}

run();
