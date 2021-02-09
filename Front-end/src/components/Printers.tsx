import axios from 'axios';
import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';

const Printers: React.FC = () => {

  // Assign data types to variables
  interface Printer {
    id: number;
    rfid_uuid: string;
    printer_name: string;
    username: string;
    name: string;
    last_access_date: string;
    status: string;
    assigned_by: string;
  }

  // Create and assign initial state for variables using react hook 'useState'
  const [printer, setPrinter] = useState<Printer[]>([]);


  // Similar to componentDidMount and componentDidUpdate:
  // To perform actions upon loading the page
  useEffect(() => {
    const loadPrinters = async () => {
      const result = await axios.get("http://localhost:8080/api/printers"); // to get available printers in DB using API 
      setPrinter(result.data.reverse());
    }
    loadPrinters();
  }, [printer]);

  // details of all available printers are rendered into a table
  // Button to edit and assign a printer to user
  return (
    <div>
      <div className="heading d-flex flex-row justify-content-center mt-5">
        <h1>3D printers status</h1>
        <Link className="btn btn-outline-primary ml-5 h-50 mt-1" to={"/printers/add"}> +</Link>
      </div>
      <div className="table-responsive">
        <table className="table border shadow">
          <thead className="thead-dark">
            <tr>
              <th scope="col">#</th>
              <th scope="col">Printer name</th>
              <th scope="col">RFID</th>
              <th scope="col">Assigned user</th>
              <th scope="col">Assigned by</th>
              <th scope="col">Last access</th>
              <th scope="col">Status</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {printer.map((item, index) => (
              <tr>
                <th scope="row">{index + 1}</th>
                <td>{item.printer_name}</td>
                <td>{item.rfid_uuid}</td>
                <td>{item.name}</td>
                <td>{item.assigned_by}</td>
                <td>{item.last_access_date}</td>
                <td> {item.status === 'Active' ?
                  <span className="material-icons green"> stop_circle </span> :
                  <span className="material-icons red">stop_circle</span>}
                </td>
                <td>
                  <Link
                    className="btn btn-outline-primary mr-2"
                    to={`/printer/edit/${item.id}`}>
                    Edit
                  </Link>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

    </div>
  );
};

export default Printers