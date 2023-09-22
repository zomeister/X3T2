import { useState, useContext } from "react"
import { Navigate } from "react-router-dom"
import { Formik, Form, Field, ErrorMessage } from "formik"
import * as yup from "yup"

import { UserContext } from "../../contexts/UserContext"
import "../../styles/Form.css"

export default function Signup() {
    const { setUser } = useContext(UserContext)

    const handleSubmitSignup = (values) => {
        fetch('/api/signup', {
            method: 'POST',
            headers: { 'content-type': 'application/json' },
            body: JSON.stringify({ ...values, })
        })
        .then(res => res.json())
        .then(userData => console.log(userData))
        .catch(err => console.error(err))
    }
    
    return (<div className="input-container">
        <h1>Signup</h1>
        <Formik onSubmit={handleSubmitSignup}
            initialValues={{
                email: "",
                username: "",
                password: ""
            }}
            validationSchema={yup.object().shape({
                email: yup.string().email("invalid email").min(4).max(200).required("email required"),
                username: yup.string().min(3).max(40).required("username required"),
                password: yup.string().required("password required")
            })}>
            <Form className="input-group">
                <div className="form-group">
                    <label htmlFor="email">Email</label>
                    <Field type="email" name="email" id="email" className="form-control" />
                </div>
                <div className="form-group">
                    <label htmlFor="username">Username</label>
                    <Field type="username" name="username" id="username" className="form-control" />
                </div>
                <div className="form-group">
                    <label htmlFor="password">Password</label>
                    <Field type="password" name="password" id="password" className="form-control" />
                </div>
                <button type="submit" className="btn btn-primary">Submit</button>
                <div className="error-group">
                    <ErrorMessage name="email" component="div" />
                    <ErrorMessage name="username" component="div" />
                    <ErrorMessage name="password" component="div" />
                </div>
            </Form>
        </Formik>
    </div>
    )
}
