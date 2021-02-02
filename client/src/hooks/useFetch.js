import {useState, useEffect, useCallback} from 'react'
import axios from 'axios';


export default url => {
  // const baseUrl = 'http://localhost:5000';
  const [isLoading, setIsLoading] = useState(false);
  const [response, setResponse] = useState(null);
  const [error, setError] = useState(null);
  const [options, setOptions] = useState({});

  const doFetch = useCallback((options = {}) => {
    setOptions(options);
    setIsLoading(true);
  }, []);

  useEffect(() => {
    let skipGetResponseAfterDestroy = false;
    if (!isLoading)
      return;

    axios(url, options)
      .then(res => {
        if (!skipGetResponseAfterDestroy) {
          setResponse(res.data);
          setIsLoading(false);
        }
      })
      .catch(error => {
        if (!skipGetResponseAfterDestroy) {
          setError(error.response ? error.response.data : error.message);
          setIsLoading(false);
        }
      });

    return () => {
      skipGetResponseAfterDestroy = true;
    }
  }, [isLoading, url, options]);

  return [{isLoading, response, error}, doFetch];
}
