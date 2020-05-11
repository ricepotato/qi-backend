# quant invest backend RESTful API Server

qi backend RESTful api Server

## resources

### /list/:market

<table>
    <tbody>
        <tr>
        <th>Resource</th>
        <td>/list/:market</td>
        </tr>
        <tr>
            <th>Method</th>
            <td>GET</td>
        </tr>
        <tr>
            <th>Request</th>
            <td>
            Path Parameter : </br>
            market : KOSDAQ, KOSPI </br><br>
            Parameter Input : </br>
            <table>
                <thead>
                    <tr>
                        <th>name</th>
                        <th>required</th>
                        <th>type</th>
                        <th>description</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td>mc_min</td>
                        <td>optional</td>
                        <td>int</td>
                        <td></td>
                    </tr>
                    <tr>
                        <td>mc_max</td>
                        <td>optional</td>
                        <td>int</td>
                        <td></td>
                    </tr>
                    <tr>
                        <td>limit</td>
                        <td>optional</td>
                        <td>int</td>
                        <td>default:20</td>
                    </tr>
                </tbody>
            </table>
            </td>
        </tr>
    </tbody>
</table>



