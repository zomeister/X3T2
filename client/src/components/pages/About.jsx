import {useState, useEffect, useContext} from "react"
import {Link, Navigate} from "react-router-dom"
import '../../styles/About.css'

import reactLogo from '../../assets/react.svg'
import reactRouterLogo from '../../assets/logos/reactRouterLogo.svg'
import threeLogo from '../../assets/logos/threeLogo.svg'
import formikLogo from '../../assets/logos/formikLogo.png'
import tailwindLogo from '../../assets/logos/tailwindLogo.png'
import postcssLogo from '../../assets/logos/postcssLogo.png'
import viteLogo from '/vite.svg'
import otherLogo from '../../assets/logo.svg'

export default function About () {
    
    const logos = [
        {id: 1, name: 'Vite', dest: 'https://vitejs.dev/', src: viteLogo, alt: 'Vite logo'},
        {id: 2, name: 'React', dest: 'https://react.dev/', src: reactLogo, alt: 'React logo'},
        {id: 3, name: 'ReactRouter', dest: 'https://reactrouter.com/en/main', src: reactRouterLogo, alt: 'React Router logo'},
        {id: 4, name: 'Formik', dest: 'https://formik.org/', src: formikLogo, alt: 'Formik logo'},
        {id: 5, name: 'Tailwind', dest: 'https://tailwindcss.com/', src: tailwindLogo, alt: 'TailwindCSS logo'},
        {id: 6, name: 'PostCSS', dest: 'https://postcss.org/docs/', src: postcssLogo, alt: 'PostCSS logo'},
        // {id: 7, name: 'Three', dest: 'https://threejs.org/docs/', src: threeLogo, alt: 'Three logo'},
    ]
    const logoLinks = logos.map((logo, index) =>
            <a href={logo.dest} target="_blank" rel="noreferrer" key={index}>
                <label>{logo.name}</label>
                <img src={logo.src} alt={logo.alt} className="logo-icon" height="70px"/>
            </a>
    )

    return (
        <div className="about-container">
            <h1>About</h1>
            <h2>Description:</h2>
            <b>Immerse yourself in this virtual pet simulator and start your X3T2 adventure!</b>
            <ul>
                <li>Adopt and care for your loyal pets!</li>
                <li>Check up and consistently care for them!</li>
                <li>Add and message friends!</li>
                <li>Work to provide for pets!</li>
            </ul>
            <br/>
            <h4>Built with:</h4>
            <div className="logo-link">
                {logoLinks}
            </div>
        </div>
    )
}
