import React from 'react';
import { Form, Input, Button, Checkbox, DatePicker, Radio, message, Typography } from 'antd';
import { useNavigate } from 'react-router-dom';

import axios from 'axios';
import './css/register.css'

const { Group: CheckboxGroup } = Checkbox;
const { Group: RadioGroup } = Radio;

const plainOptions = ['Tự nhiên', 'xã hội', 'Thể dục', 'Ngoại ngữ'];

const Register = () => {
  const navigate = useNavigate();

  const onFinish = async (values) => {
    try {
        values.group=values.group[0]
      // Gửi dữ liệu đăng ký đến server
      const response = await axios.post("http://127.0.0.1:5000/api/register", values);

      console.log(response.data);
      if (response.data) {
        message.success("Đăng ký tài khoản thành công");
        navigate('/');
      }
    } catch (error) {
      console.error("Lỗi khi gửi yêu cầu đăng ký:", error);
      message.error("Đã có lỗi xảy ra khi đăng ký tài khoản");
    }
  };

  return (
    <div className='register'>
      <Form
        className='form2'
        name="register"
        onFinish={onFinish}
        initialValues={{ gender: 'Nam', group: '' }}
        labelCol={{ span: 8 }}
        wrapperCol={{ span: 16 }}
      >
       
         <Typography.Title style={{marginLeft:'220px'}}>Đăng Ký</Typography.Title>
        <Form.Item
         style={{ marginRight: '240px', marginBottom: '16px' }} 
          label="Họ và tên"
          name="fullname"
          rules={[{ required: true, message: 'Vui lòng nhập Họ và tên!' }]}
        >
          <Input style={{marginLeft:'50px', width:'400px'}} />
        </Form.Item>

        <Form.Item
          style={{ marginRight: '300px', marginBottom: '16px' }} 
          label="Email"
          name="email"
          rules={[{ required: true, type: 'email', message: 'Vui lòng nhập địa chỉ email hợp lệ!' }]}
        >
          <Input  style={{marginLeft:'70px', width:'400px'}}/>
        </Form.Item>

        <Form.Item
         style={{ marginRight: '145px', marginBottom: '16px' }} 
          label="Tên đăng nhập"
          name="username"
          rules={[{ required: true, message: 'Vui lòng nhập tên đăng nhập!' }]}
        >
          <Input  style={{marginLeft:'18px',width:'400px'}} />
        </Form.Item>

        <Form.Item
         style={{ marginRight: '240px', marginBottom: '16px' }} 
          label="Mật khẩu"
          name="password"
          rules={[{ required: true, message: 'Vui lòng nhập mật khẩu!' }]}
        >
          <Input.Password  style={{marginLeft:'50px',width:'400px'}}/>
        </Form.Item>

        <Form.Item label="Năm sinh" name="dob"  style={{ marginRight: '240px', marginBottom: '16px' }} >
      
          <DatePicker  style={{marginLeft:'50px' ,width:'400px'}} />
        </Form.Item>

        <Form.Item label="Quê quán" name="hometown" style={{ marginRight: '240px', marginBottom: '16px' }} >
       
          <Input  style={{marginLeft:'50px',width:'400px'}}/>
        </Form.Item>

        <Form.Item label="Tổ" name="group" initialValue={[]}  style={{ marginRight: '240px', marginBottom: '16px' }} >
      
          <CheckboxGroup options={plainOptions}  style={{marginLeft:'50px',width:'400px'}} />
        </Form.Item>

        <Form.Item label="Giới tính" name="sex" style={{ marginRight: '240px', marginBottom: '16px' }}>
          
          <RadioGroup style={{marginLeft:'50px',width:'300px'}}>
            <Radio value="Nam">Nam</Radio>
            <Radio value="Nữ">Nữ</Radio>
          </RadioGroup>
        </Form.Item>

        <Form.Item wrapperCol={{ offset: 8, span: 16 }}>
          <Button type="primary" htmlType="submit" className='dky'>
            Đăng ký
          </Button>
        </Form.Item>
      </Form>
    </div>
  );
};

export default Register;
