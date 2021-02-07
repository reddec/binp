import {DefaultApi} from "./internal";
import {Configuration} from "./internal";


export const apiURL = (process.env.NODE_ENV === 'production') ? '..' : 'http://localhost:8000'

export const InternalAPI = new DefaultApi(new Configuration({
    basePath: `${apiURL}/internal`
}))