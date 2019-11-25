import axios from "axios";

axios.defaults.baseURL =
  process.env.NODE_ENV === "development"
    ? "http://localhost:8000/api/v1"
    : "/api/v1";

const getCase = async caseId => {
  try {
    const response = await axios.get(`/cases/${caseId}/`);
    console.log(response.data);
    return response.data;
  } catch (e) {
    throw Error('Case retrieval failed.');
  }
};

const myAPI = {
  getCase
};

export default myAPI;
