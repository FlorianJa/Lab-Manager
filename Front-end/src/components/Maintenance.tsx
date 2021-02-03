import axios from 'axios';
import React, { useEffect, useState } from 'react';
import { useHistory } from "react-router-dom";

const Maintenance: React.FC = () => {
  let history = useHistory();

  interface MaintenanceDetails {
    printer_name: string;
    service_interval: number;
    print_hours: number;
  }

  const [maintenance, setMaintenance] = useState<MaintenanceDetails>({
    printer_name: '',
    service_interval: 0,
    print_hours: 0
  })

  const { printer_name, service_interval, print_hours }: MaintenanceDetails = maintenance;

  const onInputChange = (e: any) => {
    const newChange = { ...maintenance, [e.target.name]: parseInt(e.target.value) }
    setMaintenance(newChange)
  }

  useEffect(() => {
    loadMaintenance();
  }, []);

  const reset_maintenance: MaintenanceDetails = {
    printer_name: "EOS",
    service_interval: maintenance.service_interval,
    print_hours: 0
  }
  const change = JSON.stringify(reset_maintenance)

  const onUpdate = async (e: any) => {
    e.preventDefault()
    try {
      await axios.put(`http://localhost:8080/api/maintenance/1`, maintenance);
      alert("Service interval updated")
    }
    catch (err) {
      alert(err.message)
    }
  };

  const onSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    console.log(reset_maintenance)
    setMaintenance(reset_maintenance)
    e.preventDefault();
    try {
      await axios.put(`http://localhost:8080/api/maintenance/1`, change);
      alert("Reset Maintenace done")
    }
    catch (err) {
      alert(err.message)
    }

    history.push("/maintenance");
  };

  const loadMaintenance = async () => {
    const maintenance = await axios.get("http://localhost:8080/api/maintenance/1");
    console.log(maintenance.data)
    setMaintenance(maintenance.data)
  };


  return (
    <div >
      <h1 className="heading d-flex flex-row justify-content-center mt-5">Maintenance</h1>
      <div className="mt-5 p-4 row justify-content-center">
        <form onSubmit={e => onSubmit(e)}>

          <div className="form-group row">
            <label htmlFor="printTime" className="col-sm-5 col-form-label">Printer Name :</label>
            <div className="col-sm-4">
              <input type="text" readOnly className="form-control-plaintext" id="printTime" value={printer_name} />
            </div>
          </div>

          <div className="form-group row">
            <label htmlFor="serviceInterval" className="col-sm-5 col-form-label">Service-interval (Hrs) :</label>
            <div className="col-sm-4">
              <input type="number" className="form-control" name="service_interval" id="serviceInterval" onChange={e => onInputChange(e)} value={service_interval} />
            </div>

            <div className="text-center">
              <button className="btn btn-warning" onClick={onUpdate}>Update</button>
            </div>
          </div>

          <div className="form-group row">
            <label htmlFor="printTime" className="col-sm-5 col-form-label">Total Print hours :</label>
            <div className="col-sm-4">
              <input type="number" readOnly className="form-control-plaintext" id="printTime" value={print_hours} />
            </div>
          </div>

          <div className="form-group row mt-5">
            <label htmlFor="remainingHrs" className="col-sm-5 col-form-label font-weight-bold"> Remaining print hours for next maintainence :</label>
            <div className="col-sm-4 mt-2">
              <input type="number" readOnly className="form-control-plaintext font-weight-bold" id="remainingHrs" value={service_interval - print_hours} />
            </div>
          </div>

          <div className="text-center mt-5 ">
            <button className="btn btn-success" >Reset</button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default Maintenance