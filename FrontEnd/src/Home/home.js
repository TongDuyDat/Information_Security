import React, { useEffect, useState } from 'react';
import { UserOutlined, FileTextOutlined } from '@ant-design/icons';
import { Layout, Menu, Form, Input, Button, FloatButton, message, Card, Row, Col, Select, Modal, theme } from 'antd';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

const storedToken = localStorage.getItem('accessToken');

const { Header, Content } = Layout;

const Home = () => {
  const [selectedLabel, setSelectedLabel] = useState(null);
  const [filteredData, setFilteredData] = useState([]);
  const [allData, setAllData] = useState([]);
  const [form1] = Form.useForm();
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [open, setOpen] = useState(false);
  const [data, setData] = useState([]);

  useEffect(() => {
    fetchDataFromApi();
  }, []);

  useEffect(() => {
    if (selectedLabel !== null) {
      filterData(selectedLabel);
    } else {
      setFilteredData(allData); // Nếu không có label được chọn, hiển thị tất cả dữ liệu
    }
  }, [selectedLabel, allData]);

  const fetchDataFromApi = async () => {
    try {
      const response = await axiosInstance.get('http://127.0.0.1:5000/api/get_posts');
      setAllData(response.data.data);
      setFilteredData(response.data.data); // Hiển thị tất cả dữ liệu khi component được tạo
    } catch (error) {
      console.error('Error fetching data:', error);
    }
  };

  const filterData = (label) => {
    const filtered = allData.filter(item => item.label === label);
    setFilteredData(filtered);
  };

  const handleLabelChange = (event) => {
    const label = event.target.value;
    setSelectedLabel(label);
  };

  const handlePublicKeyChange = (event) => {
    const file = event.target.files[0];
    setFile(file);
  };

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

  const axiosInstance = axios.create({
    baseURL: 'http://127.0.0.1:5000',
    headers: {
      'x-access-token': storedToken,
      'Content-Type': 'application/json',
    },
  });

  const submit = async () => {
    const value = form1.getFieldsValue();
    const title = value.mytitle;
    const content = value.mycontent;
    const type = value.type;

    try {
      const response = await axiosInstance.post("api/create_post", {
        title,
        content,
        post_type: type,
      }).then((dat) => {
        const formData = new FormData();
        formData.append("file", file);
        axios.post(`http://127.0.0.1:5000/api/upload_file?post_id=${dat.data.data.post_id}`, formData);
      });

      if (response.data) {
        localStorage.setItem('accessToken', response.data);
        message.success("Đăng bài thành công");
        fetchDataFromApi(); // Làm mới dữ liệu sau khi đăng bài
      }
    } catch (error) {
      console.error('Error submitting data:', error);
    }
  };

  const getData = async () => {
    try {
      const response = await axiosInstance.get('api/get_posts');
      setData(response.data.data);
    } catch (error) {
      console.error('Error fetching data:', error);
    }
  };

  const { colorBgContainer } = theme.useToken();

  return (
    <Layout style={{ height: '100vh' }}>
      <Header style={{ display: 'flex', alignItems: 'center' }}>
        <Menu theme="dark" mode="horizontal" defaultSelectedKeys={['1']}>
          <Menu.Item key="Trang chủ" onClick={() => handleLabelChange({ target: allData})}>Trang chủ</Menu.Item>
          <Menu.Item key="Tổ tự nhiên" onClick={() => handleLabelChange({ target: { value: 'Tổ tự nhiên' } })}>Tổ tự nhiên</Menu.Item>
          <Menu.Item key="Tổ xã hội" onClick={() => handleLabelChange({ target: { value: 'Tổ xã hội' } })}>Tổ xã hội</Menu.Item>
          <Menu.Item key="Tổ thể dục" onClick={() => handleLabelChange({ target: { value: 'Tổ thể dục' } })}>Tổ thể dục</Menu.Item>
          <Menu.Item key="Tổ ngoại ngữ" onClick={() => handleLabelChange({ target: { value: 'Tổ ngoại ngữ' } })}>Tổ ngoại ngữ</Menu.Item>
        </Menu>
        <div className='find' style={{ marginLeft: '400px' }}>
          <Form>
            <Input placeholder='Nhập nội dung tìm kiếm' type='text' onChange={(e) => handleLabelChange({ target: { value: e.target.value } })} />
          </Form>
        </div>
        <div background='#00FFFF'>
          <Button onClick={() => handleLabelChange({ target: { value: null } })}>Tìm kiếm</Button>
        </div>
        <div className='icon' theme="dark" style={{ marginLeft: '150px' }}>
          <Button onClick={() => navigation('/')}>
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
                  { value: 'Tổ tự nhiên', label: 'Tổ tự nhiên' },
                  { value: 'Tổ xã hội', label: 'Tổ xã hội' },
                  { value: 'Tổ ngoại ngữ', label: 'Tổ ngoại ngữ' },
                  { value: 'Tổ thể dục', label: 'Tổ thể dục' },
                  { value: 'Thông tin chung', label: 'Thông tin chung' },
                ]}
              />
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
              {filteredData.map(item => (
                <Card title={item.title} style={{ paddingBottom: 25 }}>
                  <Row>
                    <Row span={16} style={{ margin: 10 }}>
                      {item.content}
                    </Row>
                    <Row>
                      {item.image.map((element, index) => (
                        <Col span={8}>
                          <img key={index} src={element} style={{ width: 200, height: 150 }} alt={`Image ${index}`} />
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
