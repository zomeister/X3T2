import { useState, useContext, useEffect } from "react"
import { Formik, Form, Field, ErrorMessage } from "formik"
import * as yup from "yup"
import { UserContext } from "../../contexts/UserContext"

export default function OwnerForm () {
    const { user } = useContext(UserContext)

    const handleCreateProfile = (values) => {
        fetch(`/api/owners`, {
            method: 'POST',
            headers: { 'content-type': 'application/json' },
            body: JSON.stringify({ ...values, })
        })
        .then(res => res.json())
        .then(ownerData => console.log(ownerData))
        .catch(err => console.error(err))
    }

    return(<><div className="profile-form">
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
            <Form>
                <div className="form-group">
                    <label htmlFor="first-name">First Name</label>
                    <Field type="text" name="first-name" id="first-name" className="form-control" />
                    <ErrorMessage name="first-name" component="div" />
                </div>
                <div className="form-group">
                    <label htmlFor="last-name">Last Name</label>
                    <Field type="text" name="last-name" id="last-name" className="form-control" />
                    <ErrorMessage name="last-name" component="div" />
                </div>
                <div className="form-group">
                    <label htmlFor="city">City</label>
                    <Field type="text" name="city" id="city" className="form-control" />
                    <ErrorMessage name="city" component="div" />
                </div>
                <div className="form-group">
                    <label htmlFor="bio">Bio</label>
                    <Field type="text" name="bio" id="bio" className="form-control" />
                    <ErrorMessage name="bio" component="div" />
                </div>
                <div className="form-group">
                    <label htmlFor="profile-url">Profile Image</label>
                    <Field type="image" name="profile-url" id="profile-url" className="form-control" />
                    <ErrorMessage name="profile-url" component="div" />
                </div>
                <button type="submit" className="btn btn-primary">Submit</button>
            </Form>
        </Formik>
    </div>
    </>)
}