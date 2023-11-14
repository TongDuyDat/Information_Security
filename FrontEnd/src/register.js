import { Button, Form, Typography, message } from 'antd';
import './css/register.css';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

function Register(){
    const[form] = Form.useForm();
    const getData = async (e) =>{
    console.log(e);
    const username = e.namedk;
    const password = e.passdk;
    const email = e.emaildk;
    
    try {
      const response = await axios.post("http://127.0.0.1:5000/api/register", {
        username: username,
        password: password,
        email:email,
      });
      console.log(response.data);
      if(response.data){
       message.success("đăng ký tài khoản thành công");
        navigation('/');
    }
    
    } catch (error) {
      console.error("Error making the request:", error);
    }
   }
    const navigation = useNavigate();
return <div className='register' >
    <Form className='form2' form={form} onFinish={getData} >
    <div  >
        <Button className='back' onClick={()=> navigation('/')} ></Button>
    </div>
       <Typography.Title ><span className='title'>CREATE ACCOUNT</span> </Typography.Title>
    <Form.Item name={'emaildk'}>
            <input placeholder='Email' type='email'  className='a1'/>
        </Form.Item>
        <Form.Item name={'namedk'}>
            <input placeholder='User name' type='text' className='a1' name='namedk' />
        </Form.Item>
        <Form.Item name={'passdk'}>
            <input placeholder='Mật khẩu' type='password'  className='a1'/>
        </Form.Item>
        <Form.Item name={'repass'} >
            <input placeholder='Nhập lại mật khẩu' type='password' className='a1'/>
        </Form.Item>
       
        <div className='dky'>
            <Button type='primary' htmlType='submit'> ĐĂNG KÝ</Button>
        </div>
       
    </Form>
</div>
}
export default Register;