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
 * @interface Query
 */
export interface Query {
    /**
     * 
     * @type {string}
     * @memberof Query
     */
    operation?: string;
    /**
     * 
     * @type {boolean}
     * @memberof Query
     */
    failed?: boolean;
    /**
     * 
     * @type {boolean}
     * @memberof Query
     */
    pending?: boolean;
    /**
     * 
     * @type {Array<string>}
     * @memberof Query
     */
    labels?: Array<string>;
}

export function QueryFromJSON(json: any): Query {
    return QueryFromJSONTyped(json, false);
}

export function QueryFromJSONTyped(json: any, ignoreDiscriminator: boolean): Query {
    if ((json === undefined) || (json === null)) {
        return json;
    }
    return {
        
        'operation': !exists(json, 'operation') ? undefined : json['operation'],
        'failed': !exists(json, 'failed') ? undefined : json['failed'],
        'pending': !exists(json, 'pending') ? undefined : json['pending'],
        'labels': !exists(json, 'labels') ? undefined : json['labels'],
    };
}

export function QueryToJSON(value?: Query | null): any {
    if (value === undefined) {
        return undefined;
    }
    if (value === null) {
        return null;
    }
    return {
        
        'operation': value.operation,
        'failed': value.failed,
        'pending': value.pending,
        'labels': value.labels,
    };
}


