import React from "react";

const GlobalContext = React.createContext({
  sequenceData: [],
  setSequenceData: () => {},
  aisleListData: [],
  setAisleListData: () => {},
  checked: [],
  setChecked: () => {},
  expanded: [],
  setExpanded: () => {},
  itemCount: 0,
  setItemCount: () => {},
});

export default GlobalContext;
