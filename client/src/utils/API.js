import ApolloClient from "apollo-boost";

export const client = new ApolloClient({
  uri: "http://localhost:8000/graphql/"
});


// import axios from "axios";

// // export default axios.create({
// //   baseURL: "http://localhost:4000/graphql/",
// //   responseType: "json"
// // });

// export default axios.create({
//     baseURL: "http://localhost:8000/graphql/",
//     responseType: "json"
//   });