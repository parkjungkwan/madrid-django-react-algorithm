import React, {useState} from 'react'
import Badge from '@mui/material/Badge';
import MailIcon from '@mui/icons-material/Mail';
import Button from '@mui/material/Button';

export default function Counter(){
    return (<div style={{margin: 'auto 0'}}>
            <Badge badgeContent={4} color="secondary">
                <MailIcon color="action" />
            </Badge>
            <Button  variant="outlined">
                Add
            </Button>
        </div>)
}