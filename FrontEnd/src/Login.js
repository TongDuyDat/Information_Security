import { Button, Form, Space, Typography,Checkbox, message } from 'antd';
import './css/login.css';
import './css/logo.jpg';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import Item from 'antd/es/list/Item';

  
function Login(){
    const[form] = Form.useForm();
    const getData = async (e) => { 
        console.log(e);
        const username = e.myemail;
        const password = e.mypass;
        try {
          const response = await axios.post("http://127.0.0.1:5000/api/login", {
            username: username,
            password: password,
          });
          console.log(response.data);
          if(response.data.access_token){
            localStorage.setItem('accessToken', response.data.access_token);
            message.success("đăng nhập thành công");
            navigation('/Home')
          } else message.error("tên tài khoản hoặc mật khẩu không đúng");
        } catch (error) {
         
          console.error("Error making the request:", error);
        }
      }
  const navigation = useNavigate();
return <div className='login'>
 <Form className='form' form={form} onFinish={getData}>
    <Typography.Title style={{marginLeft:'100px', fontStyle:'italic', color:'#0000FF'}}>Đăng Nhập</Typography.Title>
    <Form.Item  name={'myemail'} label='Username' > 
        <input placeholder='Nhập tên tài khoản' className='email' style={{width:'280px'}} />
    </Form.Item>
    <Form.Item  name={'mypass'} label='Password' > 
        <input placeholder='Nhập mật khẩu' type='password' className='pass' style={{marginLeft:'2px', width:'280px'}}/>
    </Form.Item>
   
   <div className='dn'> <Button type='primary' htmlType='submit'  >
        ĐĂNG NHẬP
    </Button>
   
    </div>
    <div className='a' >
       bạn chưa có tài khoản ? <Button className='dk' onClick={()=> navigation("/dangky") }>Đăng Ký</Button>
    </div>
 </Form>
</div>

}
export default Login;