import React, { useContext } from "react";
import NavigationBar from "../NavigationBar";
import ShoppingList from "../ShoppingList";
import Footer from "../Footer";
import MUIDataTable from "mui-datatables";
import GlobalContext from "../../context/GlobalContext";

export default function List() {

  return (
    <div>
      <NavigationBar />
      <ShoppingList />
      <Footer />
    </div>
  );
}
