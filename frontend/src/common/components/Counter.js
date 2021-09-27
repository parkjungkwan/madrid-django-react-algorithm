import React, {useState} from 'react'
import Badge from '@mui/material/Badge';
import MailIcon from '@mui/icons-material/Mail';
import Button from '@mui/material/Button';
import styled from 'styled-components'

export default function Counter(){
    return (<CounterDiv >
            <Badge badgeContent={4} color="secondary">
                <MailIcon color="action" />
            </Badge>
            <Button  variant="outlined">
                Add
            </Button>
        </CounterDiv>)
}

const CounterDiv = styled.div`
    text-align: center;
`