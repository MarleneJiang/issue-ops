import {setFailed, setOutput} from '@actions/core';
function getRepoFromHubURL(url) {
  if (url.host !== "github.com") {
      throw "URL must be from github.com domain";
  }

  return url;
}
function run() {
    let { REPOSITORY: repository } = process.env
    if (!repository) throw new Error('REPOSITORY env var is not set')
    // repository 是否含有https://github.com/字段
    if (repository.includes('https://github.com/')) {
      try {
          // When parsed the url will be like <https://hub.docker.com>
          const url = new URL(repository.replace(/[<>]/g, ''));
          repository = getRepoFromHubURL(url);
          console.log(repository);
      } catch (e) {
          setFailed(e);
          return;
      }
  }


    setOutput('repository', repository);
}

run();
