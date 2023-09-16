import { useState, useContext, useEffect } from "react"
import { Formik, Form, Field, ErrorMessage } from "formik"
import * as yup from "yup"

import { UserContext } from "../../contexts/UserContext"

export default function Profile() {
    const { user } = useContext(UserContext)
    const [ owner, setOwner ] = useState({})
    // const [username, setUsername] = useState(user.username)

    const handleViewProfile = () => {
        fetch(`/api/profile`, {
            method: 'GET',
            headers: { 'content-type': 'application/json' },
        })
        .then(res => res.json())
        .then(ownerData => console.log(ownerData))
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
        </div>
        <div className="profile-form">
            <h1>Create Owner Profile</h1>
        </div>
    </div>
    )
}
