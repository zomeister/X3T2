import {} from "react"
import { Formik, Form, Field, ErrorMessage } from "formik"
import * as yup from "yup"

export default function AddPet () {
    const handleAddPet = (values) => {

    }

    return(<>
        <Formik onSubmit={handleAddPet}
            initialValues={{
                name: "",
                factor: 100
            }}
            validationSchema={yup.object().shape({
                name: yup.string().required("name required"),
                factor: yup.number().required("factor required"),
                strain_id: yup.number().required("strain required")
            })}
        >
            <Form>
                <div className="form-group">
                    <label htmlFor="name">Name</label>
                    <Field name="name" type="text" className="form-control" placeholder="Name" />
                    <ErrorMessage name="name" component="div" />
                </div>
                <div className="form-group">
                    <label htmlFor="factor">Factor</label>
                    <Field name="factor" type="number" className="form-control" placeholder="Factor" />
                    <ErrorMessage name="factor" component="div" />
                </div>
                <div className="form-group">
                    <label htmlFor="strain">Strain</label>
                    <Field name="strain" type="number" className="form-control" placeholder="Strain ID" />
                    <ErrorMessage name="strain" component="div" />
                </div>
                <button type="submit" className="btn btn-primary">Submit</button>
            </Form>
        </Formik>
    </>)
}