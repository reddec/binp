/* tslint:disable */
/* eslint-disable */
/**
 * BINP
 * Internal APIs
 *
 * The version of the OpenAPI document: 0.1.0
 * 
 *
 * NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).
 * https://openapi-generator.tech
 * Do not edit the class manually.
 */

import { exists, mapValues } from '../runtime';
/**
 * 
 * @export
 * @interface InvokeResult
 */
export interface InvokeResult {
    /**
     * 
     * @type {string}
     * @memberof InvokeResult
     */
    name: string;
    /**
     * 
     * @type {number}
     * @memberof InvokeResult
     */
    duration: number;
}

export function InvokeResultFromJSON(json: any): InvokeResult {
    return InvokeResultFromJSONTyped(json, false);
}

export function InvokeResultFromJSONTyped(json: any, ignoreDiscriminator: boolean): InvokeResult {
    if ((json === undefined) || (json === null)) {
        return json;
    }
    return {
        
        'name': json['name'],
        'duration': json['duration'],
    };
}

export function InvokeResultToJSON(value?: InvokeResult | null): any {
    if (value === undefined) {
        return undefined;
    }
    if (value === null) {
        return null;
    }
    return {
        
        'name': value.name,
        'duration': value.duration,
    };
}


