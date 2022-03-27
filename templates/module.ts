import {Module} from "@nestjs/common";
import { {{ clean_entity_name }} } from "./{{entity_name}}.entity";
import { TypeOrmModule } from '@nestjs/typeorm';
{% for x in imports -%}
import { {{ x[0] }} } from '{{ x[1] }}';
{% endfor %}


@Module({
	imports: [
		TypeOrmModule.forFeature([
			{{ clean_entity_name }},
			{% for x in imports -%}
			{{ x[0] }},
			{% endfor %}
		])
	],
	controllers: [],
	providers: [],
	exports: [TypeOrmModule]
})
export class {{ clean_entity_name }}Module {}
