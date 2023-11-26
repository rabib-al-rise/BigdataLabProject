import { useState, useTransition } from 'react'
import axios from "axios"
import './App.css'
import { useForm } from "react-hook-form"

function App() {
  const {
    register,
    handleSubmit,
    watch,
    formState: { errors },
  } = useForm()
  const [text, setText] = useState(0);

  const sentData=(data)=>{
    
    axios
      .post("http://localhost:5000/view", data, {
        headers: {
          "Content-Type": "application/x-www-form-urlencoded",
        },
      
      })
      .then((res) => {setText(res.data.log_prediction)})
      .catch((err) => {
        console.log(err)});

  }
  return (
    <>
     <h1 className='mb-5'>Water Quality Analysis</h1>
      <form onSubmit={handleSubmit(sentData)}>
        <label className='mr-2' htmlFor="aluminium">Aluminium:</label> 
        <input {...register("aluminium")} type="text" className="input input-bordered w-full max-w-xs mb-5"  /><br />

        <label className='mr-2' htmlFor="ammonia">Ammonia:</label> 
        <input {...register("ammonia")} type="text" className="input input-bordered w-full max-w-xs mb-5"  /><br />

        <label className='mr-2' htmlFor="arsenic">Arsenic:</label> 
        <input {...register("arsenic")} type="text" className="input input-bordered w-full max-w-xs mb-5"  /><br />

        <label className='mr-2' htmlFor="barium">Barium:</label> 
        <input {...register("barium")} type="text" className="input input-bordered w-full max-w-xs mb-5"  /><br />

        <label className='mr-2' htmlFor="cadmium">Cadmium:</label> 
        <input {...register("cadmium")} type="text" className="input input-bordered w-full max-w-xs mb-5"  /><br />

        <label className='mr-2' htmlFor="chloramine">Chloramine:</label> 
        <input {...register("chloramine")} type="text" className="input input-bordered w-full max-w-xs mb-5"  /><br />

        <label className='mr-2' htmlFor="chromium">Chromium:</label> 
        <input {...register("chromium")} type="text" className="input input-bordered w-full max-w-xs mb-5"  /><br />

        <label className='mr-2' htmlFor="copper">Copper:</label> 
        <input {...register("copper")} type="text" className="input input-bordered w-full max-w-xs mb-5"  /><br />

        <label className='mr-2' htmlFor="flouride">Flouride:</label> 
        <input {...register("flouride")} type="text" className="input input-bordered w-full max-w-xs mb-5"  /><br />

        <label className='mr-2' htmlFor="bacteria">Bacteria:</label> 
        <input {...register("bacteria")} type="text" className="input input-bordered w-full max-w-xs mb-5"  /><br />

        <label className='mr-2' htmlFor="viruses">Viruses:</label> 
        <input {...register("viruses")} type="text" className="input input-bordered w-full max-w-xs mb-5"  /><br />

        <label className='mr-2' htmlFor="lead">Lead:</label> 
        <input {...register("lead")} type="text" className="input input-bordered w-full max-w-xs mb-5"  /><br />

        <label className='mr-2' htmlFor="nitrates">Nitrates:</label> 
        <input {...register("nitrates")} type="text" className="input input-bordered w-full max-w-xs mb-5"  /><br />

        <label className='mr-2' htmlFor="nitrites">Nitrites:</label> 
        <input {...register("nitrites")} type="text" className="input input-bordered w-full max-w-xs mb-5"  /><br />

        <label className='mr-2' htmlFor="mercury">Mercury:</label> 
        <input {...register("mercury")} type="text" className="input input-bordered w-full max-w-xs mb-5"  /><br />

        <label className='mr-2' htmlFor="perchlorate">perchlorate:</label> 
        <input {...register("perchlorate")} type="text" className="input input-bordered w-full max-w-xs mb-5"  /><br />

        <label className='mr-2' htmlFor="radium">Radium:</label> 
        <input {...register("radium")} type="text" className="input input-bordered w-full max-w-xs mb-5"  /><br />

        <label className='mr-2' htmlFor="selenium">Selenium:</label> 
        <input {...register("selenium")} type="text" className="input input-bordered w-full max-w-xs mb-5"  /><br />

        <label className='mr-2' htmlFor="silver">Silver:</label> 
        <input {...register("silver")} type="text" className="input input-bordered w-full max-w-xs mb-5"  /><br />

        <label className='mr-2' htmlFor="uranium">Uranium:</label> 
        <input {...register("uranium")} type="text" className="input input-bordered w-full max-w-xs mb-5"  /><br />

        <input type="submit" className='btn btn-primary mt-5' value="Predict" />
      </form>
      <p>The prediction is : {text}</p>
    </>
  )
}

export default App
