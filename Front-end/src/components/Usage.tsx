import axios from "axios";
import React, { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import { CSVLink } from "react-csv"; // react-csv library to export data to a excel sheet

// Assign data types to variables
interface UserUsage {
  user: string;
  last_access_date: string;
  print_hours: string;
  filament_cost: string;
  operating_cost: string;
  printer_cost: string;
  additional_cost: string;
  total_cost: string;
}

// Assign data types to variables
interface UsageData {
  id: number;
  owner: string;
  file_name: string;
  print_time: string;
  time_stamp: string;
  print_status: string;
  printer_name: string;
  filament_name: string;
  filament_price: string;
  filament_weight: string;
  filament_used: string;
  filament_cost: string;
  operating_cost: string;
  printer_cost: string;
  additional_cost: string;
  total_cost: string;
}

// Assign data types to variables
interface ReportHeaders {
  label: string;
  key: string;
}

// Create and assign initial state for variables using react hook 'useState'
const Usage: React.FC = () => {
  const [usage_detail, setUsage] = useState<UsageData[]>([]);
  const [usage_report, setUsageReport] = useState<UserUsage[]>([]);

  // Headers in usage report
  const headers: ReportHeaders[] = [
    { label: "User", key: "user" },
    { label: "Last Access Date", key: "last_access_date" },
    { label: "Print Hours", key: "print_hours" },
    { label: "Filament Cost", key: "filament_cost" },
    { label: "Operating Cost", key: "operating_cost" },
    { label: "Printer Cost", key: "printer_cost" },
    { label: "Additional Cost", key: "additional_cost" },
    { label: "Total Cost(Euro)", key: "total_cost" }
  ];

  // Similar to componentDidMount and componentDidUpdate:
  // To perform actions upon loading the page
  useEffect(() => {
    const loadUsage = async () => {
      const result = await axios.get("http://localhost:8080/api/usage");
      setUsage(result.data);
      const user = await axios.get("http://localhost:8080/api/user");
      setUsageReport(user.data);
      console.log(result.data)
    }
    loadUsage();
  }, [usage_detail]); // checks change in state of usage_detail variable

  // Overview of Usage details of all usage items are rendered into a table
  // Buttons to view and edit data of each usage item
  return (
    <div>
      <div className="heading d-flex flex-row justify-content-center mt-5">
        <div>
          <h1>Usage details</h1>
        </div>
        <div>
          <CSVLink data={usage_report}  // Element to load usage_report data into excel sheet
            headers={headers}
            filename={"Usage_Data.csv"}
            className="btn btn-outline-primary export"
            target="_blank">Export</CSVLink>
        </div>
      </div>
      <div className="table-responsive">
        <table className="table border shadow">
          <thead className="thead-dark">
            <tr>
              <th scope="col">#</th>
              <th scope="col">Printer Name</th>
              <th scope="col">Username</th>
              <th scope="col">Print State</th>
              <th scope="col">Time Stamp</th>
              <th scope="col">Usage Time</th>
              <th scope="col">Total Cost (€)</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {usage_detail.map((usage, index) => (
              <tr>
                <th scope="row">{index + 1}</th>
                <td>{usage.printer_name}</td>
                <td>{usage.owner}</td>
                <td>{usage.print_status === 'PrintDone' ?
                  <span className="material-icons green">done</span> :
                  usage.print_status}
                </td>
                <td>{usage.time_stamp}</td>
                <td>{usage.print_time}</td>
                <td>{usage.total_cost}</td>
                <td>
                  <Link className="btn btn-primary mr-2" to={`/usage/${usage.id}`}>
                    View
                  </Link>
                  <Link
                    className="btn btn-outline-primary mr-2"
                    to={`/usage/edit/${usage.id}`}>
                    Edit
                  </Link>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div >);
}
export default Usage;