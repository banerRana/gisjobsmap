import React, { useState, useEffect } from "react";
import {
    Form,
    Input,
    Button,
    Icon,
    Row,
    Col,
    Tooltip,
    Switch,
    Select
} from "antd";

import { useRouter } from "../../hooks/useRouter";

import { parseJSON } from "../../utils/misc";
import { getTags, getCategories } from "../../utils/http_functions";

import {
    resetQueryParams,
    stringifyQueryParams,
    parseQueryString,
    removeEmptySearches
} from "../../utils/routing";

import { countries } from "../../config";

const formItemLayout = {
    labelCol: 8,
    wrapperCol: 16
};

const { Option } = Select;

const JobSearch = ({ isFetching, fetchData, form }) => {
    const router = useRouter();

    const { query } = router;
    const initialValues = parseQueryString(router.location.search);

    const { getFieldDecorator } = form;

    // eslint-disable-next-line no-unused-vars
    const [tags, setTags] = useState([]);

    // eslint-disable-next-line no-unused-vars
    const [categories, setCategories] = useState([]);

    const handleSearch = values => {
        const defaultsRemoved = removeEmptySearches({
            ...{
                box: query.box ? query.box : undefined
            },
            ...values
        });
        // defaultsRemoved.box = router.query.box;
        const search = stringifyQueryParams(defaultsRemoved);
        router.push({ search });
        fetchData(defaultsRemoved);
    };

    const handleSubmit = e => {
        if (e) {
            e.preventDefault();
        }
        form.validateFields((err, fieldsValue) => {
            if (err) {
                return;
            }
            handleSearch(fieldsValue);
        });
    };

    const handleReset = () => {
        form.resetFields();
        router.push({ search: resetQueryParams(router.query) });
        const { box } = router.query;
        fetchData({ box });
    };

    const populateTags = () => {
        getTags()
            .then(parseJSON)
            .then(response => {
                setTags(response.data);
            })
            .catch(error => {
                // eslint-disable-next-line no-undef
                console.log("get tags error: ", error);
                setTags([]);
            });
    };

    const populateCategories = () => {
        getCategories()
            .then(parseJSON)
            .then(response => {
                setCategories(response.data);
            })
            .catch(error => {
                // eslint-disable-next-line no-undef
                console.log("populate categories error: ", error);
                setCategories([]);
            });
    };

    const handleDateChange = val => {
        handleSearch({ ...router.query, date: val });
    };

    const handleMapOnlyChange = checked => {
        handleSearch({ ...router.query, maponly: checked });
    };

    const handleCountryChange = val => {
        handleSearch({ ...router.query, box: undefined, country: val });
    };

    useEffect(() => {
        // handleTagSearch();
        if (!tags.length) {
            populateTags();
        }
        if (!categories.length) {
            populateCategories();
        }
    }, []);
    return (
        <div style={{ width: "275px", textAlign: "left" }}>
            <Form
                onSubmit={handleSubmit}
                {...formItemLayout}
                labelAlign="left"
                size="small"
            >
                <Row>
                    <Col span={24}>
                        <Form.Item
                        //style={{ marginBottom: "10px" }}
                        // labelCol={{ span: 8 }}
                        // wrapperCol={{ span: 16 }}
                        // label="Search"
                        >
                            {getFieldDecorator("q", {
                                initialValue: initialValues.q
                                    ? initialValues.q
                                    : "",
                                rules: [{ required: false }]
                            })(
                                <Input
                                    placeholder="Enter Search Term"
                                    size="large"
                                    disabled={isFetching}
                                    // suffix={<Icon type="search" />}
                                />
                            )}
                        </Form.Item>
                    </Col>
                </Row>
                <Row>
                    <Col span={24}>
                        <Form.Item
                            labelCol={{ span: 20 }}
                            wrapperCol={{ span: 4 }}
                            label={
                                <span>
                                    Search Map Only&nbsp;
                                    <Tooltip title="100% remote jobs will not be included in the results.">
                                        <Icon type="info-circle-o" />
                                    </Tooltip>
                                </span>
                            }
                        >
                            {getFieldDecorator("maponly", {
                                valuePropName: "checked",
                                initialValue: initialValues.maponly
                                    ? initialValues.maponly
                                    : false,
                                // initialValues.mapOnly
                                //     ? initialValues.mapOnly
                                //     : false,
                                rules: [{ required: false }]
                            })(
                                <Switch
                                    onChange={(checked, evt) =>
                                        handleMapOnlyChange(checked, evt)
                                    }
                                />
                            )}
                        </Form.Item>
                    </Col>
                </Row>
                <Row>
                    <Col span={24}>
                        <Form.Item
                            labelCol={{ span: 8 }}
                            wrapperCol={{ span: 16 }}
                            label="Country"
                        >
                            {getFieldDecorator("country", {
                                initialValue: initialValues.country
                                    ? initialValues.country
                                    : "any",
                                rules: [{ required: false }]
                            })(
                                <Select
                                    showSearch
                                    onChange={handleCountryChange}
                                >
                                    <Select.Option key="any" value="any">
                                        Any
                                    </Select.Option>
                                    {Object.keys(countries).map(key => {
                                        return (
                                            <Select.Option
                                                key={key}
                                                value={key}
                                            >
                                                <span
                                                    className={`flag-icon flag-icon-${key}`}
                                                />{" "}
                                                {countries[key]}
                                            </Select.Option>
                                        );
                                    })}
                                </Select>
                            )}
                        </Form.Item>
                    </Col>
                </Row>
                <Row>
                    <Col span={24}>
                        <Form.Item
                            labelCol={{ span: 8 }}
                            wrapperCol={{ span: 16 }}
                            validateStatus={null}
                            label="Categories"
                        >
                            {getFieldDecorator("categories", {
                                initialValue: initialValues.categories
                                    ? initialValues.categories
                                    : [],
                                rules: [
                                    {
                                        type: "array",
                                        required: false
                                    }
                                ]
                            })(
                                <Select
                                    getPopupContainer={triggerNode =>
                                        triggerNode.parentNode
                                    }
                                    disabled={isFetching}
                                    placeholder="Any"
                                    mode="multiple"
                                >
                                    {categories.length
                                        ? categories.map(item => {
                                              return (
                                                  <Option
                                                      key={item.id}
                                                      value={item.name}
                                                  >
                                                      {item.name}
                                                  </Option>
                                              );
                                          })
                                        : null}
                                </Select>
                            )}
                        </Form.Item>
                    </Col>
                </Row>
                <Row>
                    <Col span={24}>
                        <Form.Item
                            labelCol={{ span: 8 }}
                            wrapperCol={{ span: 16 }}
                            // style={{ marginBottom: "10px" }}
                            validateStatus={null}
                            label="Tags"
                        >
                            {getFieldDecorator("tags", {
                                initialValue: initialValues.tags
                                    ? initialValues.tags
                                    : [],
                                rules: [
                                    {
                                        type: "array",
                                        required: false
                                    }
                                ]
                            })(
                                <Select
                                    getPopupContainer={triggerNode =>
                                        triggerNode.parentNode
                                    }
                                    disabled={isFetching}
                                    placeholder="Any"
                                    mode="multiple"
                                >
                                    {tags.length
                                        ? tags.map(item => {
                                              return (
                                                  <Option
                                                      key={item.id}
                                                      value={item.name}
                                                  >
                                                      {item.name}
                                                  </Option>
                                              );
                                          })
                                        : null}
                                </Select>
                            )}
                        </Form.Item>
                    </Col>
                </Row>
                <Row>
                    <Col span={24}>
                        <Form.Item
                            labelCol={{ span: 12 }}
                            wrapperCol={{ span: 12 }}
                            // style={{ marginBottom: "20px" }}
                            validateStatus={null}
                            label="Date Posted"
                        >
                            {getFieldDecorator("date", {
                                initialValue: initialValues.date
                                    ? initialValues.date
                                    : "0",
                                rules: [{ required: false }]
                            })(
                                <Select
                                    disabled={isFetching}
                                    getPopupContainer={triggerNode =>
                                        triggerNode.parentNode
                                    }
                                    onChange={handleDateChange}
                                    placeholder="All"
                                >
                                    <Option value="0">Any</Option>
                                    <Option value="1">Past day</Option>
                                    <Option value="3">Past 3 days</Option>
                                    <Option value="7">Past week</Option>
                                    <Option value="14">Past 2 weeks</Option>
                                    <Option value="30">Past month</Option>
                                </Select>
                            )}
                        </Form.Item>
                    </Col>
                </Row>
                {/* <Row style={{ display: expanded ? "block" : "none" }} gutter={[0, 0]}>
          <Col span={24}>
            <Form.Item
              style={{ margin: "0" }}
              label={
                <span>
                  Remote / Telecommute &nbsp;
                  <Tooltip title="These results will not display on the map, only in the list.">
                    <Icon type="info-circle-o" />
                  </Tooltip>
                </span>
              }
            >
              {getFieldDecorator("remote", {
                initialValue: initialValues.remote
                  ? initialValues.remote
                  : "include",
                rules: [{ required: false }]
              })(
                <Radio.Group onChange={handleRemoteRadioChange}>
                  <Radio.Button value="include">Include</Radio.Button>
                  <Radio.Button value="exclude">Exclude</Radio.Button>
                  <Radio.Button value="only">Only Remote</Radio.Button>
                </Radio.Group>
              )}
            </Form.Item>
          </Col>

          <Col span={24} style={{ margin: 0, padding: 0 }}>
            <Form.Item
              style={{ margin: "0" }}
              validateStatus={null}
              label="Category"
            >
              {getFieldDecorator("categories", {
                initialValue: initialValues.categories
                  ? initialValues.categories
                  : [],
                rules: [
                  {
                    type: "array",
                    required: false
                  }
                ]
              })(
                <Select
                  getPopupContainer={triggerNode => triggerNode.parentNode}
                  disabled={isFetching}
                  placeholder="Any"
                  mode="multiple"
                >
                  {categories.length
                    ? categories.map(item => {
                      return (
                        <Option key={item.id} value={item.name}>
                          {item.name}
                        </Option>
                      );
                    })
                    : null}
                </Select>
              )}
            </Form.Item>
          </Col>

          <Col span={24}>
            <Form.Item
              style={{ margin: "0" }}
              validateStatus={null}
              label="Tags"
            >
              {getFieldDecorator("tags", {
                initialValue: initialValues.tags ? initialValues.tags : [],
                rules: [
                  {
                    type: "array",
                    required: false
                  }
                ]
              })(
                <Select
                  getPopupContainer={triggerNode => triggerNode.parentNode}
                  disabled={isFetching}
                  placeholder="Any"
                  mode="multiple"
                >
                  {tags.length
                    ? tags.map(item => {
                      return (
                        <Option key={item.id} value={item.name}>
                          {item.name}
                        </Option>
                      );
                    })
                    : null}
                </Select>
              )}
            </Form.Item>
          </Col>

          <Col span={24}>
            <Form.Item
              style={{ margin: "0", marginBottom: "10px" }}
              validateStatus={null}
              label="Date Posted"
            >
              {getFieldDecorator("date", {
                initialValue: initialValues.date ? initialValues.date : "0",
                rules: [{ required: false }]
              })(
                <Select
                  disabled={isFetching}
                  getPopupContainer={triggerNode => triggerNode.parentNode}
                  onChange={handleDateChange}
                  placeholder="All"
                >
                  <Option value="0">Any</Option>
                  <Option value="1">Past day</Option>
                  <Option value="3">Past 3 days</Option>
                  <Option value="7">Past week</Option>
                  <Option value="14">Past 2 weeks</Option>
                  <Option value="30">Past month</Option>
                </Select>
              )}
            </Form.Item>
          </Col>
        </Row> */}

                <Row>
                    <Col span={8}>
                        {/* <a
              style={{ marginLeft: 8, fontSize: 12 }}
              onClick={() => setExpanded(!expanded)}
            >
              Advanced <Icon type={expanded ? "up" : "down"} />
            </a> */}
                    </Col>
                    <Col span={16} style={{ textAlign: "right" }}>
                        <Button
                            size="default"
                            onClick={handleReset}
                            disabled={isFetching}
                            style={{ marginRight: "10px" }}
                        >
                            Reset
                        </Button>
                        <Button
                            size="default"
                            loading={isFetching}
                            type="primary"
                            htmlType="submit"
                        >
                            Apply
                        </Button>
                    </Col>
                </Row>
            </Form>
        </div>
    );
};

export const WrappedJobSearchForm = Form.create({ name: "search_form" })(
    JobSearch
);
