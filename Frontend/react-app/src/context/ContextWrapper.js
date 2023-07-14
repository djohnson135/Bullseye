import React, { useState, useEffect } from "react";
import GlobalContext from "./GlobalContext";

export default function ContextWrapper(props) {
  const [sequenceData, setSequenceData] = useState([]);
  const [aisleListData, setAisleListData] = useState([]);
  const [checked, setChecked] = useState([]);
  const [expanded, setExpanded] = useState([]);
  const [itemCount, setItemCount] = useState(0);

  return (
    <GlobalContext.Provider
      value={{
        sequenceData,
        setSequenceData,
        aisleListData,
        setAisleListData,
        checked,
        setChecked,
        expanded,
        setExpanded,
        itemCount,
        setItemCount,
      }}
    >
      {props.children}
    </GlobalContext.Provider>
  );
}
