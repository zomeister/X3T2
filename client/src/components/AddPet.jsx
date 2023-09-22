import {} from "react"
import { Formik, Form, Field, ErrorMessage} from "formik"
import * as yup from "yup"
import "../styles/Form.css"

export default function AddPet () {

    const handleAddPet = (values) => {
        fetch('/api/shelter', {
            method: 'POST',
            headers: { 'content-type': 'application/json' },
            body: JSON.stringify({ ...values, })
        })
        .then(res => {
            if (res.ok) {
                return res.json()
            } else {
                return 'error occurred'
            }
        })
        .then(userData => console.log(userData))
        .catch(err => console.error(err))
    }

    return(<div className="input-container">
        <Formik onSubmit={handleAddPet}
            initialValues={{
                name: "",
                factor: "100"
            }}
            validationSchema={yup.object().shape({
                name: yup.string().required("name required"),
                factor: yup.number().required("factor required"),
                strain_id: yup.number().required("strain required")
            })}
        >
            <Form className="input-group">
                <div className="form-group">
                    <label htmlFor="name">Name</label>
                    <Field name="name" type="text" className="form-control" placeholder="Name" />
                </div>
                <div className="form-group">
                    <label htmlFor="factor">Factor</label>
                    <Field name="factor" type="number" className="form-control" placeholder="Factor" />
                </div>
                <div className="form-group">
                    <label htmlFor="strain_id">Strain</label>
                    <Field name="strain_id" type="number" className="form-control" placeholder="Strain ID" />
                </div>
                <button type="submit" onClick={handleAddPet} className="btn btn-primary">Submit</button>
                <div className="error-group">
                    <ErrorMessage name="name" component="div" />
                    <ErrorMessage name="factor" component="div" />
                    <ErrorMessage name="strain" component="div" />
                </div>
            </Form>
        </Formik>
    </div>)
}