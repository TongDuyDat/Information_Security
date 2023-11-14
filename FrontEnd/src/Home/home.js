import React, { useEffect, useState } from 'react';
import { LaptopOutlined, NotificationOutlined, UserOutlined, EditOutlined } from '@ant-design/icons';
import { Breadcrumb, Layout, Menu, theme, Form, Input, Button, FloatButton, message, Upload, Card, Row, Col } from 'antd';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import { FileTextOutlined, FileAddOutlined } from '@ant-design/icons';
import { Select, Modal } from 'antd';



const storedToken = localStorage.getItem('accessToken');

const { Header, Content, Sider } = Layout;
const items1 = ['Trang chủ', 'Tổ tự nhiên', 'Tổ xã hội', 'Tổ thể dục', 'Tổ ngoại ngữ'].map((key) => ({
  key,
  label: `${key}`,
  
}));



const Home = () => {
   
    const [selectedLabel, setSelectedLabel] = useState(null);
    const [filteredData, setFilteredData] = useState([]);
  
    useEffect(() => {
      // Call API with the selected label when it changes
      if (selectedLabel !== null) {
        fetchDataFromApi(selectedLabel);
      }
    }, [selectedLabel]);
  
    const fetchDataFromApi = async (label) => {
      try {
        // Make API call to fetch filtered data based on the selected label
        const response = await fetch(`http://127.0.0.1:5000/api/search_post?label=${label}`);
        const data = await response.json();
        setFilteredData(data);
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    };

    const handleLabelChange = (event) => {
      const label = event.target.value;
      setSelectedLabel(label);
    };
  const [form1] = Form.useForm();
  const [file, setfile] = useState();
  const handlePublicKeyChange = (event) => {
    const file = event.target.files[0];
    setfile(file);
  };
  const [loading, setLoading] = useState(false);
  const [open, setOpen] = useState(false);
  const showModal = () => {
    setOpen(true);
  };

  const handleOk = () => {
    setLoading(true);
    setTimeout(() => {
      setLoading(false);
      setOpen(false);
    }, 3000);
  };
  const handleCancel = () => {
    setOpen(false);
  };
  const navigation = useNavigate();
  const [data, setData] = useState([])
  useEffect(() => {
    getData();
  }, []);
  const axiosInstance = axios.create({
    baseURL: 'http://127.0.0.1:5000',
    headers: {
      'x-access-token': storedToken,
      'Content-Type': 'application/json',
    },
  });
  const submit = async (e) => {
    const value = form1.getFieldsValue();
    console.log(value);
    const title = value.mytitle;
    const content = value.mycontent;
    const type = value.type;
    try {
      const response = await axiosInstance.post("api/create_post", {
        title,
        content,
        post_type: type,
      })
        .then((dat) => {
          const formData = new FormData();
          formData.append("file", file)
          axios.post(`http://127.0.0.1:5000/api/upload_file?post_id=${dat.data.data.post_id}`, formData)
          // console.log('test',dat);
        });
      if (response.data) {
        localStorage.setItem('accessToken', response.data);
        message.success("đăng bài thành công");

      }
    } catch {

    }
  };
  const getData = async () => {
    axiosInstance.get('api/get_posts')
      .then(response => {
        setData(response.data.data);
        console.log(response.data);
      })
      .catch(error => {
        // Xử lý lỗi nếu có
        console.error(error);
      });
  }

 
  const {
    token: { colorBgContainer },
  } = theme.useToken();
  return (
    <Layout style={{ height: '100vh' }}>
      <Header
        style={{
          display: 'flex',
          alignItems: 'center',
        }}

      >
      
        <div className="demo-logo" />
        <Menu theme="dark" mode="horizontal" defaultSelectedKeys={['1']} items={items1} />
        <div className='find' style={{ marginLeft: '400px' }}>
          <form >
            <Input placeholder='nhập nội dung tìm kiếm' type='text' />
          </form>
        </div>
        <div background='#00FFFF'>
          <Button >
            Tìm kiếm
          </Button>
        </div>
        <div className='icon' theme="dark" style={{ marginLeft: '150px' }}>
          <Button onClick={() => navigation('/')} >
            <UserOutlined style={{ color: '#000000', fontSize: '20px' }} />LogOut
          </Button>
        </div>
      </Header>
      <>
        <Modal
          width={'700px'}
          open={open}
          title="Đăng Bài"
          onOk={handleOk}
          onCancel={handleCancel}
          footer={[
            <input
              type="file"
              accept=".*"
              id="privateKeyFile"
              onChange={handlePublicKeyChange}
            />,
            <Button key="back" onClick={handleCancel}>
              Hủy
            </Button>,
            <Button htmlType='submit' type="primary" onClick={submit} >
              Đăng bài
            </Button>,
          ]}
        >
          <Form className='form1' form={form1} >
            <Form.Item name={'mytitle'}>
              <textarea placeholder='Tiêu đề bài viết' style={{ width: '650px' }} />
            </Form.Item>
            <Form.Item name={'type'}>
              <Select
                showSearch
                style={{
                  width: 200,
                  marginBottom: 5,
                  marginTop: 5
                }}
                placeholder="Chọn thể loại"
                optionFilterProp="children"
                filterOption={(input, option) => (option?.label ?? '').includes(input)}
                filterSort={(optionA, optionB) =>
                  (optionA?.label ?? '').toLowerCase().localeCompare((optionB?.label ?? '').toLowerCase())
                }
                options={[
                  {
                    value: 'Tổ tự nhiên',
                    label: 'Tổ tự nhiên',
                  },
                  {
                    value: 'Tổ xã hội',
                    label: 'Tổ xã hội',
                  },
                  {
                    value: 'Tổ ngoại ngữ',
                    label: 'Tổ ngoại ngữ',
                  },
                  {
                    value: 'Tổ thể dục',
                    label: 'Tổ thể dục',
                  },
                  {
                    value: 'Thông tin chung',
                    label: 'Thông tin chung'
                  },
                  
                ]}

              />
                  items1(onClick={handleLabelChange});
            </Form.Item>
            <Form.Item name={'mycontent'}>
              <textarea placeholder='Nội dung bài viết' style={{ width: '650px', height: '450px' }} />
            </Form.Item>
          </Form>
        </Modal>
      </>
      <Layout>

        <Layout
          style={{
            padding: '0 24px 24px',
          }}
        >
          <Content
            style={{
              padding: 24,
              margin: 0,
              minHeight: 280,
              background: colorBgContainer,
            }}
          >
            <FloatButton
              icon={<FileTextOutlined onClick={showModal} type='primary' />}
              description="ĐĂNG BÀI"
              shape="square"
              style={{
                right: 24,
              }}
            />
            <div>

              {data.map(item => (
                <Card title={item.title} style={{ paddingBottom: 25 }}>
                  <Row>
                  <Row span={16} style={{margin:10}}>
                    {item.content}
                  </Row>
                  <Row>
                    {item.image.map((element, index) => (
                      <Col span={8}>
                        <img key={index} src={element} style={{ width: 200, height: 150 }} />
                      </Col>
                    ))}
                  </Row>
                  </Row>
                </Card>
              ))}

            </div>
          </Content>
        </Layout>
      </Layout>
    </Layout>
  );

};

export default Home;