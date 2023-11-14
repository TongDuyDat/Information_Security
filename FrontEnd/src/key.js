import { Button, Input, Typography } from "antd";
import { Checkbox, Divider } from 'antd';
import React, { useState } from 'react';
import {ArrowLeftOutlined  } from '@ant-design/icons';
import { useNavigate } from "react-router-dom";

const CheckboxGroup = Checkbox.Group;
const plainOptions = ['Tự nhiên', 'xã hội', 'Thể dục','Ngoại ngữ'];


function Key() {
    const Navigate = useNavigate();
    const [checkedList, setCheckedList] = useState('');
    const indeterminate = checkedList.length > 0 && checkedList.length < plainOptions.length;
    const onChange = (list) => {
        setCheckedList(list);
    };
    return <div className="register">
        <form style={{height:'350px', width:'450px', backgroundColor:'azure', borderRadius:'15px' }} >
        <ArrowLeftOutlined style={{marginLeft:'20px', marginTop:'20px'}} onClick={() => Navigate('/')}/>
            <Typography style={{ textAlign: 'center', marginTop:'15px', textSizeAdjust:'50' }}>THÔNG TIN NGƯỜI DÙNG </Typography>
            <form name="khoa" >
                <div style={{width:'400px', marginLeft:'25px', marginTop:'10px'}}>
                    <Input type="text" placeholder="Họ tên" style={{marginBottom:'15px', marginTop:'15px'}}>
                    </Input>
                    <Input type="text" placeholder="Quê quán" style={{marginBottom:'15px'}}/>
                    <Input type="number" placeholder="Số cccd" style={{marginBottom:'15px'}}/>
                    <label style={{marginRight:'5px'}}>
                        Tổ :
                    </label>
                    <CheckboxGroup options={plainOptions} value={checkedList} onChange={onChange} />
                    <Button type="primary" htmlType="submit" style={{marginLeft:'150px', marginTop:'20px', width:'100px'}}>
                        Gửi
                    </Button>
                </div>
            </form>
        </form>
    </div>
}
export default Key;