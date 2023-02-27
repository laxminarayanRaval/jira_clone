import React from 'react';

import { Button } from 'shared/components';

import { Header, BoardName } from './Styles';

const ProjectBoardHeader = () => (
  <Header>
    <BoardName>Kanban board</BoardName>
    <a
      style={{ display: 'none' }}
      href="https://github.com/laxminarayanRaval/jira_clone"
      target="_blank"
      rel="noreferrer noopener"
    >
      <Button icon="github">Github Repo</Button>
    </a>
  </Header>
);

export default ProjectBoardHeader;
