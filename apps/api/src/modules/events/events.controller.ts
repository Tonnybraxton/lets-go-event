import { Controller, Get, Query } from "@nestjs/common";
import { ApiQuery, ApiTags } from "@nestjs/swagger";
import { EventsService } from "./events.service.js";

@ApiTags("events")
@Controller("events")
export class EventsController {
  constructor(private readonly events: EventsService) {}
  @Get("locations")
  @ApiQuery({ name: "q", minLength: 2 })
  locations(@Query("q") query = "") { return query.trim().length < 2 ? [] : this.events.autocomplete(query.trim()); }
  @Get("nearby")
  @ApiQuery({ name: "location", example: "westlands-nairobi" })
  @ApiQuery({ name: "radius", required: false, example: 25 })
  nearby(@Query("location") location = "westlands-nairobi", @Query("radius") radius = "25", @Query("category") category?: string) {
    const radiusKm = Math.min(100, Math.max(2, Number(radius) || 25));
    return this.events.nearby(location, radiusKm, category);
  }
}
