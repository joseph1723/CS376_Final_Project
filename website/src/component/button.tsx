import React from 'react';
import styled from 'styled-components';
import axios from 'axios';

const Wrapper = styled.div`
  width: 200px;
  height: 60px;
  border-radius: 8px;
  background-color: #98b4d4;
  padding: 8px 16px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  font-size: 16px;
  font-weight: bold;
  color: #ffffff;
  cursor: pointer;

  &:hover {
    box-shadow: 4px 4px 4px #cccccccc;
  }
`;

interface Props {
  req: string;
  setRes: (res: string) => void;
}

const Button = ({ req, setRes }: Props) => {
  const detection = async () => {
    try {
      const res = await axios.get(`http://localhost:8000/model?data=${req}`);

      console.log(res);

      setRes(res.data as string);
    } catch (error) {
      console.log(error);
    }
  };

  // eslint-disable-next-line @typescript-eslint/no-misused-promises
  return <Wrapper onClick={detection}>Run Model</Wrapper>;
};

export default Button;
