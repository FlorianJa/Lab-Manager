import React, { useState, useEffect } from "react";
import axios from "axios";
import { useHistory, useParams } from "react-router-dom";

const EditPrinter: React.FC = () => {

    // Assign data types to variables
    interface Printer {
        rfid_uuid: string;
        printer_name: string;
        username: string;
        name: string;
        assigned_by: string;
    }

    let history = useHistory();
    const { id } = useParams<{ id: string }>();
    // Create and assign initial state for variables using react hook 'useState'
    const [printer, setPrinter] = useState<Printer>({
        rfid_uuid: '',
        printer_name: '',
        username: '',
        name: '',
        assigned_by: ''
    })

    // Creating variables inheriting types from interface Printer
    const { rfid_uuid, printer_name, username, name, assigned_by }: Printer = printer;

    // To update new changes in varaibles
    const onInputChange = (e: any) => {
        const newChange = { ...printer, status: 'Inactive', [e.target.name]: e.target.value }
        setPrinter(newChange)
    }

    // Similar to componentDidMount and componentDidUpdate:
    // To perform actions upon loading the page
    useEffect(() => {
        loadPrinter();
    }, []);

    // When clicked on Add, the form data is posted to DB via API 
    const onSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
        e.preventDefault();
        console.log(printer)
        try {
            await axios.put(`http://localhost:8080/api/printers/${id}`, printer);
            history.push("/printers");
            alert("Printer Assigned Successfully")
        }
        catch (err) {
            alert(err.message)
        }
    };

    // Get printer detail from DB based on the id of the printer
    const loadPrinter = async () => {
        const response = await axios.get(`http://localhost:8080/api/printers/${id}`);
        console.log(response.data)
        setPrinter(response.data)
    };

    // Form to update the details of the printer
    // Assigning a user to a printer by filling in the form data
    return (
        <div className="container">
            <h1 className="heading d-flex flex-row justify-content-center mt-5">Printer allocation</h1>
            <div className="mt-5 p-4 row justify-content-center">
                <form onSubmit={e => onSubmit(e)}>

                    <div className="form-group row">
                        <label htmlFor="printer_name" className="col-sm-5 col-form-label font-weight-bold">Printer Name :</label>
                        <div className="col-sm-7">
                            <input type="text" readOnly className="form-control-plaintext font-weight-bold" id="printer_name" value={printer_name} />
                        </div>
                    </div>


                    <div className="form-group row">
                        <label htmlFor="rfid_uuid" className="col-sm-5 col-form-label">RFID :</label>
                        <div className="col-sm-7">
                            <input type="text" readOnly className="form-control-plaintext" id="rfid_uuid" value={rfid_uuid} />
                        </div>
                    </div>

                    <div className="form-group row">
                        <label htmlFor="username" className="col-sm-5 col-form-label">Username :</label>
                        <div className="col-sm-7">
                            <input type="text" className="form-control" name="username" id="username" onChange={e => onInputChange(e)} value={username} />
                        </div>

                    </div>

                    <div className="form-group row">
                        <label htmlFor="name" className="col-sm-5 col-form-label">Full Name:</label>
                        <div className="col-sm-7">
                            <input type="text" className="form-control" name="name" id="name" onChange={e => onInputChange(e)} value={name} />
                        </div>
                    </div>


                    <div className="form-group row">
                        <label htmlFor="assigned_by" className="col-sm-5 col-form-label">Assigned by:</label>
                        <div className="col-sm-7">
                            <input type="text" className="form-control" name="assigned_by" id="assigned_by" onChange={e => onInputChange(e)} value={assigned_by} />
                        </div>
                    </div>

                    <div className="text-center mt-5 ">
                        <button className="btn btn-warning" >Update</button>
                    </div>
                </form>
            </div>
        </div>
    );
};

export default EditPrinter;
