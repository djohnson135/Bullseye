import React, { useState, useContext, useEffect } from "react";
import CheckboxTree from "react-checkbox-tree";
import "react-checkbox-tree/lib/react-checkbox-tree.css";
import GlobalContext from "../context/GlobalContext";
import { authorize, backend_url } from "./Global";
import "./AisleListSection.css";

function AisleListSection(props) {
  const {
    sequenceData,
    setSequenceData,
    aisleListData,
    checked,
    setChecked,
    expanded,
    setExpanded,
    itemCount,
    setItemCount,
  } = useContext(GlobalContext);

  useEffect(() => {
    setItemCount(checked.length);
  }, [checked]);

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
      <div className="aisle-list-wrapper">
        <center>
          <div className="aisle-list-header-wrapper">
            <div className="aisle-list-header">
              <p>
                Sequence of Your <span className="aisle-list-red">Order</span>
              </p>
            </div>
          </div>

          <div className="items-center justify-center flex flex-col font-semibold h-full w-full p-[-5%]">
            <div className="py-[2%]">
              Items Gathered: {itemCount}/{aisleListData.length}
            </div>
            <CheckboxTree
              iconsClass="fa5"
              icons={{
                check: <span className="rct-icon rct-icon-check" />,
                uncheck: <span className="rct-icon rct-icon-uncheck" />,
                halfCheck: <span className="rct-icon rct-icon-half-check" />,
                expandClose: (
                  <span className="rct-icon rct-icon-expand-close" />
                ),
                expandOpen: <span className="rct-icon rct-icon-expand-open" />,
                expandAll: <span className="rct-icon rct-icon-expand-all" />,
                collapseAll: (
                  <span className="rct-icon rct-icon-collapse-all" />
                ),
                parentClose: (
                  <span className="material-icons-outlined cursor-pointer text-gray-600 mx-2">
                    visibility_off
                  </span>
                ),
                parentOpen: (
                  <span className="material-icons-outlined cursor-pointer text-gray-600 mx-2">
                    visibility
                  </span>
                ),
                leaf: <span className=""></span>,
              }}
              nodes={sequenceData.slice(0, -1)}
              checked={checked}
              expanded={expanded}
              onCheck={(checkedData) => {
                setChecked(checkedData);
              }}
              onExpand={(expandedData) => {
                setExpanded(expandedData);
              }}
            />
          </div>
        </center>
      </div>
    </div>
  );
}
else {
  return (
    <div>
    <div className="aisle-list-wrapper">
      <center>
        <div className="aisle-list-header-wrapper">
          <div className="aisle-list-header">
            <p>
              Sequence of Your <span className="aisle-list-red">Order</span>
            </p>
          </div>
        </div>

        <div className="items-center justify-center flex flex-col font-semibold h-full w-full p-[-5%]">
          <div className="py-[2%]">
            Items Gathered: {itemCount}/{aisleListData.length}
          </div>
          <CheckboxTree
            iconsClass="fa5"
            icons={{
              check: <span className="rct-icon rct-icon-check" />,
              uncheck: <span className="rct-icon rct-icon-uncheck" />,
              halfCheck: <span className="rct-icon rct-icon-half-check" />,
              expandClose: (
                <span className="rct-icon rct-icon-expand-close" />
              ),
              expandOpen: <span className="rct-icon rct-icon-expand-open" />,
              expandAll: <span className="rct-icon rct-icon-expand-all" />,
              collapseAll: (
                <span className="rct-icon rct-icon-collapse-all" />
              ),
              parentClose: (
                <span className="material-icons-outlined cursor-pointer text-gray-600 mx-2">
                  visibility_off
                </span>
              ),
              parentOpen: (
                <span className="material-icons-outlined cursor-pointer text-gray-600 mx-2">
                  visibility
                </span>
              ),
              leaf: <span className=""></span>,
            }}
            nodes={sequenceData.slice(0, -1)}
            checked={checked}
            expanded={expanded}
            onCheck={(checkedData) => {
              setChecked(checkedData);
            }}
            onExpand={(expandedData) => {
              setExpanded(expandedData);
            }}
          />
        </div>
      </center>
    </div>
  </div>
);
}
}

export default AisleListSection;
