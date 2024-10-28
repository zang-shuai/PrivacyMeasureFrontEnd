import request from "./request";

export const submitFormData = async (formData: any) => {
    const formDataToSend = new FormData();
    Object.keys(formData).forEach(key => {
        formDataToSend.append(key, formData[key].content);
    });

    try {
        const response = await request.post('http://localhost:8000/api/ldp_measure', formDataToSend, {
            headers: {'Content-Type': 'multipart/form-data'}
        });
// @ts-ignore
        console.log("debug 后端返回的数据", response.response_data)
// @ts-ignore
        return response.response_data;
    } catch (error) {
        console.error(error);
        throw error;
    }
    //
    // return {
    //     id: "1726219649",
    //     code: "1",
    //     message: "评估成功",
    //     result: "2.561674454156165154186",
    //     inputs_n: "10000",
    //     input_kinds_n: "50"
    // }
};