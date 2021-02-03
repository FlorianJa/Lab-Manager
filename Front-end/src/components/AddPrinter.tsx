import React, { useState } from "react";
import axios from "axios";
import { useHistory } from "react-router-dom";

const EditPrinter: React.FC = () => {
    let history = useHistory();

    interface Printer {
        rfid_uuid: string;
        printer_name: string;
        username: string;
        name: string;
        assigned_by: string;
    }
    const [printer, setPrinter] = useState<Printer>({
        rfid_uuid: '',
        printer_name: '',
        username: '',
        name: '',
        assigned_by: ''
    })

    const { rfid_uuid, printer_name, username, name, assigned_by }: Printer = printer;

    const onInputChange = (e: any) => {
        const newPrinter = { ...printer, [e.target.name]: e.target.value }
        setPrinter(newPrinter)
    }

    const onSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
        e.preventDefault();
        const newPrinter = JSON.stringify(printer)
        console.log(newPrinter)
        try {
            await axios.post(`http://localhost:8080/api/printers`, newPrinter)
            history.push("/printers");
            alert("New printer added successfully")
        }
        catch (err) {
            alert(err.message)
        }

    };

    return (
        <div className="container">
            <h1 className="heading d-flex flex-row justify-content-center mt-5">Add Printer</h1>
            <div className="mt-5 p-4 row justify-content-center">
                <form onSubmit={e => onSubmit(e)}>

                    <div className="form-group row">
                        <label htmlFor="printer_name" className="col-sm-5 col-form-label">Printer Name :</label>
                        <div className="col-sm-7">
                            <input type="text" className="form-control" name="printer_name" id="printer_name" onChange={e => onInputChange(e)} value={printer_name} />
                        </div>
                    </div>


                    <div className="form-group row">
                        <label htmlFor="rfid_uuid" className="col-sm-5 col-form-label">RFID :</label>
                        <div className="col-sm-7">
                            <input type="text" className="form-control" name="rfid_uuid" id="rfid_uuid" onChange={e => onInputChange(e)} value={rfid_uuid} />
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
                        <button className="btn btn-success" >Submit</button>
                    </div>
                </form>

            </div>
        </div>
    );
};

export default EditPrinter;
