import { useState, useContext } from "react"
import { Navigate } from "react-router-dom"
import { Formik, Form, Field, ErrorMessage } from "formik"
import * as yup from "yup"

import { UserContext } from "../../contexts/UserContext"
import "../../styles/Form.css"

export default function Login() {
    
    const { user, setUser } = useContext(UserContext)
    const [error, setError] = useState(null)

    const handleSubmitLogin = (values) => {
        fetch('/api/login', {
            method: 'POST',
            headers: { 'content-type': 'application/json' },
            body: JSON.stringify({ ...values, })
        })
        .then(res => {
            if (res.status === 200) {
                return res.json()
            } else if (res.status === 404) {
                setError("invalid username or password")
            } else if (res.status === 401) {
                setError("invalid password")
            } else {
                setError("something went wrong and idk why")
            }
        })
        .then(userData => setUser(userData))
        .catch(err => console.error(err))
    }

    return (
    <div className="input-container">
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
            <Form className="input-group">
                <div className="form-group">
                    <label htmlFor="username">Email/Username</label>
                    <Field type="username" name="username" id="username" className="form-control" />
                </div>
                <div className="form-group">
                    <label htmlFor="password">Password</label>
                    <Field type="password" name="password" id="password" className="form-control" />
                </div>
                <button type="submit" className="btn btn-primary">Submit</button>
                <div className="error-group">
                    {error ? <p>{error}</p> : null}
                    <ErrorMessage name="username" component="div" />
                    <ErrorMessage name="password" component="div" />
                </div>
            </Form>
        </Formik>
        {user? <Navigate to="/profile" /> : null}
    </div>
    )
}