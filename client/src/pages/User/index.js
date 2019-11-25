import React from 'react';
import userImg from "../../assests/avataar.svg";
import "../../assests/styles/userStyle.css";
import jwt_decode from 'jwt-decode'
import background from "../../assests/background-event.jpg";
import styled from "styled-components";
import Avatar ,{ ConfigProvider } from 'react-avatar';
import { useFetch, SubmitRequest } from "./Backendhooks"; //to handle fetch data request from flask







const Styles = styled.div`
 .jumbo{
    // background: url(${background}) no-repeat fixed bottom;
    background-color: #7eb3c794;
    color:black;
    margin-top: 0px;
    margin-bottom: 5px;
    max-width: 80%;
    margin-left: 12%;
    &:hover{
        background-color: #69a8af;
    }
 };
 .container{
    background: url(${background}) no-repeat fixed bottom;
    max-width: inherit;
    min-height: 85vh;
    padding-right: 350px;
    padding-left: 350px;
    margin-right: auto;
    margin-left: auto;
 };

 .jumbo h2{
  font-size: 30px;
  }

 .jumbo p{
   font-size: 18px;
  }

 .jumbo li{
   list-style-type: none;
  }`;



  
    
      
  
  
   
       

															
									   

  const User = () => {
    
    const [user, offered_rides, requested_rides, hasErrors] = useFetch(); // to call flask/backend server		
    const token = ()  =>  localStorage.usertoken;
    const decoded = () => {jwt_decode(token)
    this.setState({
      first_name: decoded.identity.first_name,
      last_name: decoded.identity.last_name,
      email: decoded.identity.email
    })
  }
    return (
        <div className="container-fluid">
         <Styles>

              <div className="container">
                <div className="jumbotron mt-1">
                  <div className="col-sm-8 mx-auto">
                    <h1 className="text-center">User Profile</h1>
                    
                  </div>
                  <table className="table col-md-6 mx-auto">
                    <tbody>
                      <tr>
                        <td>Fist Name</td>
                        <td>{jwt_decode(localStorage.usertoken).identity.first_name}</td>
                        {/* <td>Neelesh Mungoli</td> */}
                      </tr>
                      <tr>
                        <td>Last Name</td>
                        {/* <td>Mungoli</td> */}
                        <td>{jwt_decode(localStorage.usertoken).identity.last_name}</td>
                      </tr>

                      
                      <tr>
                        <td>Email</td>
                        <td>{jwt_decode(localStorage.usertoken).identity.email}</td>
                        
                      </tr>
                    </tbody>
                  </table>
                </div>
              </div>

            </Styles>

            <div className="row mt-5 w-75 mx-auto">
                <div className="col-lg-6 lg-offset-6">
                    <div className="user-offered-rides">
                        <p className="heading-req">Your Offered Rides</p>
                        <ul className="list-group">
                            {offered_rides.length> 0 ?
                                <>{offered_rides.map(ride => (
                                <li className="list-group-item bg-light" key={ride.request_id}>
                                    <p className="float-left p-rider">Name: {ride.name}</p>
                                    <p className="float-left p-rider">Contact: {ride.contact_no}</p>
                                    <p className="float-left p-rider">Email: {ride.email}</p>
                                    { ride.status === 'pending' ? <>
                                    <button onClick={async () => await SubmitRequest(ride.request_id, "declined")} type="button" className="btn btn-dark btn-sm float-right font-weight-bold" > 
                                        Decline 
                                    </button>&nbsp;
                                    <button onClick={async () => await SubmitRequest(ride.request_id, "accepted")} type="button" className="btn btn-dark btn-sm float-right mr-2 font-weight-bold"  >
                                        Accept
                                    </button>
                                    </>
                                    : 
                                    <button type="button" className="btn btn-dark btn-sm float-right mr-2 font-weight-bold" disabled>
                                        Already Accepted!
                                    </button>
                                    }
                                </li>
                            ))}
                            </> : <> <p className="float-left p-rider">No Rides Offered....</p> </>}
                        </ul>
                    </div>
                </div> 
                <div className="col-lg-6 lg-offset-6">
                    <div className="user-requested-rides">
                        <p className="heading-req">Your Requested Rides</p>
                        <ul className="list-group">
                            { requested_rides.length > 0 ?
                            <>
                            {requested_rides.map(ride => (
                                <li className="list-group-item bg-light" key={ride.request_id}>
                                    <p className=" p-rider">Host Name: {ride.name}</p>
                                    { ride.status==="pending" ? 
                                    <span className="text-warning float-right">Pending</span> 
                                    : ride.status==="accepted" ?
                                    <span className="text-danger float-right mr-2">Accepted</span>
                                    :
                                    <span className="text-success float-right mr-2">Declined</span>
                                    }
                                </li>
                            ))}
                            </> : <> <p className="float-left p-rider">No Rides Requested....</p> </>}
                        </ul>
                    </div>
                </div>
            </div>
        </div>  
    )
};

export default User;