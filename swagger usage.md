swagger usage

for manual query params
```
@swagger_auto_schema(manual_parameters=[
        openapi.Parameter("start_date", openapi.IN_QUERY,
                          type=openapi.FORMAT_DATE),
        openapi.Parameter("end_date", openapi.IN_QUERY,
                          type=openapi.FORMAT_DATE)
    ])
```
for taking body of a post request 
```
@swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
        'product_slugs': openapi.Schema(type=openapi.TYPE_STRING, description='product_slugs')
    }))
```

for taking body of a post request with serializer (this one is the prefered method of all)

```
@swagger_auto_schema(request_body=AuthTokenSerializer)
```