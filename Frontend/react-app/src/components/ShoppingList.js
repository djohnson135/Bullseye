import React, { useContext } from "react";
import MUIDataTable from "mui-datatables";
import GlobalContext from "../context/GlobalContext";
import { useState, useEffect } from "react";
import { authorize, backend_url } from "./Global";
import "./ShoppingList.css";

function ShoppingList() {
  const { aisleListData } = useContext(GlobalContext);
  const columns = ["Item", "Aisle", "Price"];

  const options = {
    download: false,
    filter: false,
    viewColumns: false,
    rowsPerPage: 20,
    rowsPerPageOptions: [20, 50, 100],
    selectableRowsHeader: false,
    selectToolbarPlacement: "none",
    selectableRowsOnClick: false,
    selectableRowsHideCheckboxes: false,
    selectableRows: "none",
    sort: false,
    responsive: "scrollMaxHeight",
    tableBodyMaxHeight: "60vh",
    tableBodyHeight: "60vh"
  };

  const [user, setUser] = useState(null);

  useEffect(() => {
    const request = {
      mode: "cors",
      method: "GET",
      headers: {
        Authorization: "Bearer " + authorize.access_token,
        "Access-Control-Allow-Origin": "*"
      },
      credentials: "include",
    };
    fetch(`${backend_url}/user/`, request)
      .then((response) => response.json())
      .then((data) => setUser(data));
  }, []);

  if (authorize.userLoggedIn === false) {
  return (
    <div>
      <div className="shopping-list-wrapper">
        <center>
          <div className="shopping-list-header-wrapper">
            <div className="shopping-list-header">
              <p>
                Your <span className="shopping-list-red">Target</span> Shopping
                List
              </p>
            </div>
          </div>
          <div className="flex flex-col items-center justify-center">
            <div className="pb-[8%] w-2/3">
              <MUIDataTable
                data={aisleListData}
                columns={columns}
                options={options}
              />
            </div>
          </div>
        </center>
      </div>
    </div>
  );
  }
  else {
    return (
      <div>
        <div className="shopping-list-wrapper-signIn">
          <center>
            <div className="shopping-list-header-wrapper">
              <div className="shopping-list-header">
                <p>
                  Your <span className="shopping-list-red">Target</span> Shopping
                  List
                </p>
              </div>
            </div>
            <div className="flex flex-col items-center justify-center">
              <div className="pb-[8%] w-2/3">
                <MUIDataTable
                  data={aisleListData}
                  columns={columns}
                  options={options}
                />
              </div>
            </div>
          </center>
        </div>
      </div>
    );
  }
}

export default ShoppingList;
