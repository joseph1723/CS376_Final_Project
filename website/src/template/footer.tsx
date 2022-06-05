import React from 'react';
import styled from 'styled-components';

const Container = styled.div`
  width: 100%;
  height: 72px;
  padding: 16px 32px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: flex-end;

  .title {
    font-size: 16px;
    font-weight: bold;
    margin-bottom: 6px;
  }
  span {
    font-size: 14px;
    white-space: pre;
  }
`;

const Footer = () => {
  return (
    <Container>
      <span className={'title'}>22 Spring / Team 23</span>
      <span>20180679 : 최우진 | 20190074 : 김동근 | 20160502 : 이재희 | 20160791 : 권용빈</span>
    </Container>
  );
};

export default Footer;
