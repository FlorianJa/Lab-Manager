import React, { useState, useEffect } from "react";
import axios from "axios";

// Create and assign initial state for variables using react hook 'useState'
const Configuration: React.FC = () => {
  const [printer, setPrinter] = useState<string[]>([])
  const [operating, setOperating] = useState<string[]>([])
  const { price_printer, lifespan, maintainence_cost }: any = printer;
  const { power_consumption, electricity_cost }: any = operating;
  const [filament, setFilament] = useState<string[]>(["PLA"])
  const [filament_data, setFilamentData] = useState<string[]>([])

  // Creating variables
  let { filament_weight, filament_price, filament_name }: any = filament_data

  // To update new changes in varaibles
  const onInputChange = (e: any) => {
    const newChange = { ...printer, [e.target.name]: e.target.value }
    setPrinter(newChange)

    const newChangeOperating = { ...operating, [e.target.name]: e.target.value }
    setOperating(newChangeOperating)

    const newFilament = { ...filament_data, [e.target.name]: e.target.value }
    setFilamentData(newFilament)
  }

  // To update new changes in filament data from UI
  const handleFilament = (event: any) => {
    console.log(event.target.value)
    const set_filament = event.target.value
    setFilament(set_filament)
  }

  // Similar to componentDidMount and componentDidUpdate:
  // To perform actions upon loading the page
  useEffect(() => {
    loadPrinter();
    loadFilament();
    loadOperating();
  }, [filament]);

  // printer, operating, filament default configurations are updated in db posting data via API
  const onSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    try {
      await axios.put(`http://localhost:8080/api/printer/2`, printer);
      await axios.put(`http://localhost:8080/api/operating/2`, operating);
      await axios.put(`http://localhost:8080/api/filament/${filament}`, filament_data);
      alert("Default Configuration updated")
    }
    catch (err) {
      alert(err.message)
    }
  };

  // Get default printer configuration from DB into local variable
  const loadPrinter = async () => {
    const printer_data = await axios.get("http://localhost:8080/api/printer/2");
    setPrinter(printer_data.data)
  };

  // Get default operating configuration from DB into local variable
  const loadOperating = async () => {
    const operating_data = await axios.get("http://localhost:8080/api/operating/2");
    setOperating(operating_data.data)
  }

  // Get default filament configuration from DB into local variable
  const loadFilament = async () => {
    const filament_result = await axios.get(`http://localhost:8080/api/filament/${filament}`);
    console.log(filament_result.data)
    setFilamentData(filament_result.data)
  }

  // Form element allowing changes to Filament, Operating, Printer default configuration details
  return (
    <div className="container">
      <h1 className="heading d-flex flex-row justify-content-center mt-5">Default configuration</h1>
      <form onSubmit={e => onSubmit(e)}>
        <div className="mx-auto mt-5 p-4 shadow ">
          <h2 className="text-center mb-4">Filament Details</h2>
          <div className="form-row">
            <div className="col-md-4">
              <div >
                <label className="" htmlFor="select-filament">Filament Type</label>
              </div>
              <select className="custom-select has-tooltip"
                name="select-filament" id="select-filament" data-tooltip="Which type of filament did you use?" onChange={handleFilament} value={filament_name} data-tippy-placement="top">
                <option value="PLA" >PLA</option>
                <option value="PETG">PETG</option>
                <option value="ASA">ASA</option>
                <option value="PC-Blend">PC-Blend</option>
                <option value="Other">Other</option>
              </select>
            </div>
            <div className="col-md-4 mb-3">
              <label htmlFor="filament_price">Filament price (€)</label>
              <input type="number"
                step=".01"
                className="form-control"
                name="filament_price" placeholder="Filament price"
                onChange={e => onInputChange(e)}
                value={filament_price} required />
            </div>
            <div className="col-md-4 mb-3">
              <label htmlFor="filament_weight">Filament weight (g)</label>
              <input type="number"
                step=".01"
                className="form-control"
                name="filament_weight" placeholder="Filament weight"
                onChange={e => onInputChange(e)}
                value={filament_weight} required />
            </div>
          </div>
        </div>
        <div className="p-4 mt-5 shadow">

          <h5 className="text-left">Printer Name: EOS</h5>
          <h2 className="text-center mb-4">Printer details</h2>

          <div className="form-group row">
            <div className="col-md-4 mb-3">
              <label htmlFor="price_printer">Printer price (€)</label>
              <input type="number" className="form-control"
                name="price_printer" onChange={e => onInputChange(e)}
                placeholder="Printer price" value={price_printer} required />
            </div>
            <div className="col-md-4 mb-3">
              <label htmlFor="lifespan">Lifespan (Hrs)</label>
              <input type="number"
                className="form-control"
                name="lifespan" placeholder="Lifespan"
                onChange={e => onInputChange(e)}
                value={lifespan} required />
            </div>
            <div className="col-md-4 mb-3">
              <label htmlFor="maintainence_cost">Maintainence cost (€)</label>
              <input type="number"
                step=".01"
                className="form-control"
                name="maintainence_cost" placeholder="Maintainence cost"
                onChange={e => onInputChange(e)}
                value={maintainence_cost} required />
            </div>
          </div>
          <h2 className="text-center mb-4">Operating details</h2>
          <div className="form-group row justify-content-center">
            <div className="col-md-4 mb-3">
              <label htmlFor="power_consumption">Power consumption (kW)</label>
              <input type="number" className="form-control" step=".01"
                name="power_consumption" onChange={e => onInputChange(e)}
                placeholder="Power consumption" value={power_consumption} required />
            </div>
            <div className="col-md-4 mb-3">
              <label htmlFor="electricity_cost">Electricity Cost (€/kW)</label>
              <input type="number"
                step=".01"
                className="form-control"
                name="electricity_cost" placeholder="Electricity Cost"
                onChange={e => onInputChange(e)}
                value={electricity_cost} required />
            </div>
          </div>
        </div>

        <div className="text-center mt-5">
          <button className="btn btn-warning">Update</button>
        </div>
      </form>
    </div>
  );
};

export default Configuration