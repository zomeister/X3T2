import { useState, useContext, useEffect } from "react"
import { Formik, Form, Field, ErrorMessage } from "formik"
import * as yup from "yup"

import { UserContext } from "../../contexts/UserContext"
import "../../styles/Form.css"

export default function Profile() {
    const { user } = useContext(UserContext)
    // const [username] = useState(user.username)
    const [owner, setOwner] = useState({})
    // const { firstName, lastName } = owner

    const handleCreateProfile = (values) => {
        fetch(`/api/owners`, {
            method: 'POST',
            headers: { 'content-type': 'application/json' },
            body: JSON.stringify({ ...values, })
        })
        .then(res => res.json())
        .then(ownerData => setOwner(ownerData))
        .catch(err => console.error(err))
    }

    const handleViewProfile = () => {
        fetch(`/api/profile`, {
            method: 'GET',
            headers: { 'content-type': 'application/json' },
        })
        .then(res => {
            if (res.status === 200) {
                return res.json()
            }
        })
        .then(ownerData => setOwner(ownerData))
        .catch(err => console.error(err))
    }



    // const handleEditProfile = (values) => {
    //     fetch(`/api/${username}/owner`, {
    //         method: 'PATCH',
    //         headers: { 'content-type': 'application/json' },
    //         body: JSON.stringify({...values, })
    //     })
    //     .then(res => res.json())
    //     .then(ownerData => console.log(ownerData))
    //     .catch(err => console.error(err))
    // }
    useEffect(() => {
        handleViewProfile()
    }, [])

    return (<div>
        <div className="profile-display">
            <h1>Profile</h1>
            <div className="profile-info">
                {/* <p>Name: {firstName} {owner.last_name}</p> */}
            </div>
        </div>
        <div className="profile-form input-group">
            <h1>Create Owner Profile</h1>
            <Formik onSubmit={handleCreateProfile}
                initialValues={{
                    firstName: "",
                    lastName: "",
                    city: "",
                    bio: "",
                    profile_url: ""
                }}
                validationSchema={yup.object().shape({
                    firstName: yup.string().min(1).max().required("first name required"),
                    lastName: yup.string().min(1).max().required("last name required"),
                    city: yup.string().min(1).max(120, "City name too long.").required("city required"),
                    bio: yup.string().min(1).max(4000, "Bio too long."),
                    profile_url: yup.string().min(1).max(2800, "Profile URL too long.")
            })}>
            <Form className="input-group">
                <div className="form-group">
                    <label htmlFor="first-name">First Name</label>
                    <Field type="text" name="first-name" id="first-name" className="form-control" />
                </div>
                <div className="form-group">
                    <label htmlFor="last-name">Last Name</label>
                    <Field type="text" name="last-name" id="last-name" className="form-control" />
                </div>
                <div className="form-group">
                    <label htmlFor="city">City</label>
                    <Field type="text" name="city" id="city" className="form-control" />
                </div>
                <div className="form-group">
                    <label htmlFor="bio">Bio</label>
                    <Field type="text" name="bio" id="bio" className="form-control" />
                </div>
                <div className="form-group">
                    <label htmlFor="profile-url">Profile Image</label>
                    <Field type="image" name="profile-url" id="profile-url" className="form-control" />
                </div>
                <button type="submit" className="btn btn-primary">Submit</button>
                <div className="error-group">
                    <ErrorMessage name="first-name" component="div" />
                    <ErrorMessage name="last-name" component="div" />
                    <ErrorMessage name="city" component="div" />
                    <ErrorMessage name="bio" component="div" />
                    <ErrorMessage name="profile-url" component="div" />
                </div>
            </Form>
            </Formik>
        </div>
    </div>
    )
}
