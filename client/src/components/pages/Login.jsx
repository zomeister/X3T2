import { useState, useContext } from "react"
import { Formik, Form, Field, ErrorMessage } from "formik"
import * as yup from "yup"

import { UserContext } from "../../contexts/UserContext"

export default function Login() {
    
    const { setUser } = useContext(UserContext)

    const handleSubmitLogin = (values) => {
        fetch('/api/login', {
            method: 'POST',
            headers: { 'content-type': 'application/json' },
            body: JSON.stringify({ ...values, })
        })
        .then(res => res.json())
        .then(userData => setUser(userData))
        .catch(err => console.error(err))
    }

    return (<div>
        <h1>Login</h1>
        <Formik onSubmit={handleSubmitLogin}
            initialValues={{
                username: "",
                password: ""
            }}
            validationSchema={yup.object().shape({
                username: yup.string().required("username required"),
                password: yup.string().required("password required")
            })}>
            <Form>
                <div className="form-group">
                    <label htmlFor="username">Email/Username</label>
                    <Field type="username" name="username" id="username" className="form-control" />
                    <ErrorMessage name="username" component="div" />
                </div>
                <div className="form-group">
                    <label htmlFor="password">Password</label>
                    <Field type="password" name="password" id="password" className="form-control" />
                    <ErrorMessage name="password" component="div" />
                </div>
                <button type="submit" className="btn btn-primary">Submit</button>
            </Form>
        </Formik>
    </div>
    )
}