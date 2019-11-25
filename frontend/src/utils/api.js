import axios from "axios";

axios.defaults.baseURL =
  process.env.NODE_ENV === "development"
    ? 'http://localhost:8000/api/v1/'
    : '/api/v1/';

const search = async query => {
  try {
    const response = await axios.get(`search?q=${query}`);
    return response.data;
  } catch (e) {
    throw Error("Search failed.");
  }
};

const getCase = async caseId => {
  try {
    const response = await axios.get(`cases/${caseId}`);
    return response.data;
  } catch (e) {
    throw Error("Case retrieval failed.");
  }
};

const getDocketEntry = async docketEntryId => {
  try {
    const response = await axios.get(`docket-entries/${docketEntryId}`);
    return response.data;
  } catch (e) {
    throw Error("Getting Docket Entry failed.")
  }
};

const myAPI = {
  search,
  getCase,
  getDocketEntry
};

export default myAPI;
